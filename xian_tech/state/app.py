import asyncio
import os
import re
import time
from typing import Any, TypedDict

import reflex as rx
from dotenv import load_dotenv

from ..contact_email import send_contact_email
load_dotenv()

EMAIL_PATTERN = re.compile(
    r"^(?=.{3,254}$)(?=.{1,64}@)[A-Z0-9](?:[A-Z0-9._%+-]{0,62}[A-Z0-9])?@"
    r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}$",
    re.IGNORECASE,
)


class CommandAction(TypedDict):
    id: str
    title: str
    subtitle: str
    category: str
    badge: str
    href: str
    external: bool
    keywords: list[str]


class CommandSection(TypedDict, total=False):
    type: str
    category: str
    id: str
    title: str
    subtitle: str
    badge: str
    href: str
    external: bool
    keywords: list[str]


class ActiveCommandInfo(TypedDict):
    id: str
    title: str
    subtitle: str
    category: str
    badge: str
    href: str
    external: bool
    keywords: list[str]
    placeholder: bool


class RoadmapCard(TypedDict):
    id: str
    number: int
    title: str
    status: str
    url: str
    tags: list[str]
    tags_text: str
    golden: bool


class RoadmapColumn(TypedDict):
    id: str
    name: str
    count: int
    cards: list[RoadmapCard]


class State(rx.State):
    """Global application state."""

    mobile_nav_open: bool = False
    nav_hover_label: str = ""
    command_palette_open: bool = False
    command_palette_visible: bool = False
    command_query: str = ""
    command_palette_active_id: str | None = None
    image_lightbox_open: bool = False
    image_lightbox_src: str = ""
    image_lightbox_alt: str = ""
    copied_code_key: str = ""
    roadmap_loading: bool = False
    roadmap_error: str = ""
    roadmap_columns: list[RoadmapColumn] = []
    roadmap_done_cards: list[RoadmapCard] = []
    roadmap_done_count: int = 0
    contact_submission_inflight: bool = False
    contact_status: str = ""
    contact_error: str = ""
    contact_email_error: str = ""
    contact_message_error: str = ""
    contact_form_email: str = ""
    contact_form_message: str = ""
    contact_last_sent_at: float = 0.0
    contact_cooldown_remaining: int = 0
    contact_form_key: int = 0

    @rx.var
    def roadmap_show_loading(self) -> bool:
        """Show skeletons while the roadmap data is still empty."""
        return self.roadmap_loading or (not self.roadmap_columns and not self.roadmap_error)

    def toggle_mobile_nav(self):
        """Toggle the mobile navigation drawer."""
        self.mobile_nav_open = not self.mobile_nav_open

    def close_mobile_nav(self):
        """Close the mobile navigation."""
        self.mobile_nav_open = False

    def set_nav_hover(self, label: str):
        """Track which nav item is hovered."""
        self.nav_hover_label = label

    def clear_nav_hover(self):
        """Clear nav hover state."""
        self.nav_hover_label = ""

    async def open_command_palette(self):
        """Show the command palette."""
        if self.command_palette_open and self.command_palette_visible:
            return
        self.command_palette_visible = True
        self.command_palette_open = False
        actions = self.command_palette_actions
        self.command_palette_active_id = actions[0]["id"] if actions else None
        yield
        self.command_palette_open = True

    async def close_command_palette(self):
        """Hide the command palette and reset the query."""
        self.command_palette_open = False
        self.command_query = ""
        self.command_palette_active_id = None
        yield
        await asyncio.sleep(0.3)
        self.command_palette_visible = False

    def set_command_query(self, value: str):
        """Update the palette query."""
        self.command_query = value
        actions = self.command_palette_actions
        self.command_palette_active_id = actions[0]["id"] if actions else None

    def set_command_palette_selection(self, value: str):
        """Highlight a palette item."""
        self.command_palette_active_id = value

    def command_palette_move_up(self):
        """Move selection to previous item in the palette."""
        actions = self.command_palette_actions
        if not actions:
            return
        ids = [a["id"] for a in actions]
        current = self.command_palette_active_id
        if current is None or current not in ids:
            self.command_palette_active_id = ids[-1]
        else:
            idx = ids.index(current)
            self.command_palette_active_id = ids[idx - 1] if idx > 0 else ids[-1]

    def command_palette_move_down(self):
        """Move selection to next item in the palette."""
        actions = self.command_palette_actions
        if not actions:
            return
        ids = [a["id"] for a in actions]
        current = self.command_palette_active_id
        if current is None or current not in ids:
            self.command_palette_active_id = ids[0]
        else:
            idx = ids.index(current)
            self.command_palette_active_id = ids[idx + 1] if idx < len(ids) - 1 else ids[0]

    def open_image_lightbox(self, src: str, alt: str = ""):
        """Show the image lightbox."""
        self.image_lightbox_open = True
        self.image_lightbox_src = src
        self.image_lightbox_alt = alt

    def close_image_lightbox(self):
        """Hide the image lightbox."""
        self.image_lightbox_open = False
        self.image_lightbox_src = ""
        self.image_lightbox_alt = ""

    async def copy_code_with_feedback(self, code: str, key: str):
        """Copy code and briefly show copied feedback for the selected key."""
        self.copied_code_key = ""
        yield
        self.copied_code_key = key
        yield rx.set_clipboard(code)
        await asyncio.sleep(1.2)
        if self.copied_code_key == key:
            self.copied_code_key = ""

    async def load_roadmap(self):
        """Load the Fizzy roadmap board into state."""
        if self.roadmap_loading:
            return

        column_name_overrides = {
            "specification": "Design",
            "working on": "Execute",
            "testing": "Validate",
        }

        self.roadmap_loading = True
        self.roadmap_error = ""
        yield

        def fetch_board() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
            from ..fizzy_api import get_board_cards, get_board_columns

            token = os.getenv("FIZZY_TOKEN", "").strip()
            account_slug = (
                os.getenv("FIZZY_ACCOUNT_SLUG", "")
                or os.getenv("FIZZY_ACCOUNT", "")
                or "1"
            ).strip().lstrip("/")
            board_id = (
                os.getenv("FIZZY_BOARD_ID", "")
                or os.getenv("FIZZY_BOARD", "")
                or "03fiomkit5oknquymk0ooi26m"
            ).strip()
            base_url = (
                os.getenv("FIZZY_BASE_URL", "")
                or os.getenv("FIZZY_API_URL", "")
                or "https://tasks.xian.technology"
            ).strip()

            if not token:
                raise ValueError("Missing FIZZY_TOKEN for Fizzy API access.")
            if not account_slug or not board_id:
                raise ValueError("Missing FIZZY_ACCOUNT_SLUG or FIZZY_BOARD_ID.")

            def normalize_id(value: Any) -> str:
                return str(value).strip()

            def parse_bool(value: Any) -> bool:
                if isinstance(value, bool):
                    return value
                if value is None:
                    return False
                if isinstance(value, (int, float)):
                    return value != 0
                text = str(value).strip().lower()
                if text in {"true", "1", "yes", "y", "on"}:
                    return True
                if text in {"false", "0", "no", "n", "off", ""}:
                    return False
                return bool(value)

            columns = get_board_columns(
                base_url=base_url,
                account_slug=account_slug,
                token=token,
                board_id=board_id,
            )
            open_cards = get_board_cards(
                base_url=base_url,
                account_slug=account_slug,
                token=token,
                board_id=board_id,
            )
            closed_cards = get_board_cards(
                base_url=base_url,
                account_slug=account_slug,
                token=token,
                board_id=board_id,
                indexed_by="closed",
            )

            columns = [col for col in columns if isinstance(col, dict)]
            open_cards = [card for card in open_cards if isinstance(card, dict)]
            closed_cards = [card for card in closed_cards if isinstance(card, dict)]
            board_id_value = str(board_id)

            def is_same_board(card: dict[str, Any]) -> bool:
                board = card.get("board") or {}
                if board.get("id") is not None:
                    return str(board.get("id")) == board_id_value
                if card.get("board_id") is not None:
                    return str(card.get("board_id")) == board_id_value
                return True

            open_cards = [card for card in open_cards if is_same_board(card)]
            closed_cards = [card for card in closed_cards if is_same_board(card)]

            columns_sorted = sorted(
                columns,
                key=lambda col: (col.get("position") is None, col.get("position") or 0),
            )
            cards_by_column: dict[str, list[dict[str, Any]]] = {
                normalize_id(col.get("id", "")): []
                for col in columns_sorted
            }
            untriaged: list[dict[str, Any]] = []
            done_cards: list[dict[str, Any]] = []
            done_card_ids: set[str] = set()

            def extract_tags(raw_tags: Any) -> list[str]:
                if not raw_tags:
                    return []
                if isinstance(raw_tags, list):
                    if raw_tags and isinstance(raw_tags[0], dict):
                        return [
                            str(tag.get("name", "")).strip()
                            for tag in raw_tags
                            if tag.get("name")
                        ]
                    return [str(tag).strip() for tag in raw_tags if str(tag).strip()]
                return [str(raw_tags).strip()]

            excluded_tags_raw = os.getenv("FIZZY_EXCLUDE_TAGS", "").strip()
            excluded_tags = {
                tag.strip().lower()
                for tag in excluded_tags_raw.split(",")
                if tag.strip()
            }

            def is_excluded(card: dict[str, Any]) -> bool:
                if not excluded_tags:
                    return False
                tags = [tag.lower() for tag in extract_tags(card.get("tags"))]
                return any(tag in excluded_tags for tag in tags)

            def build_raw_card_payload(data: dict[str, Any], *, force_closed: bool = False) -> dict[str, Any]:
                tags = extract_tags(data.get("tags"))
                return {
                    "id": data.get("id", ""),
                    "number": data.get("number", 0),
                    "title": data.get("title", ""),
                    "status": str(data.get("status", "")),
                    "url": data.get("url", ""),
                    "tags": tags,
                    "tags_text": ", ".join(tags),
                    "golden": bool(data.get("golden", False)),
                    "closed": force_closed or parse_bool(data.get("closed", False)),
                }

            def add_done_payload(payload: dict[str, Any]) -> None:
                card_id = str(payload.get("id", ""))
                if not card_id or card_id in done_card_ids:
                    return
                done_cards.append(payload)
                done_card_ids.add(card_id)

            for card in open_cards:
                column_id = None
                column = card.get("column") or {}
                if card.get("column_id") is not None:
                    column_id = normalize_id(card.get("column_id"))
                elif column.get("id") is not None:
                    column_id = normalize_id(column.get("id"))

                card_payload = build_raw_card_payload(card)
                if card_payload.get("closed"):
                    add_done_payload(card_payload)
                    continue
                if is_excluded(card):
                    continue
                if column_id and column_id in cards_by_column:
                    cards_by_column[column_id].append(card_payload)
                else:
                    untriaged.append(card_payload)

            for column_id, items in cards_by_column.items():
                items.sort(key=lambda item: item["number"])

            for card in closed_cards:
                add_done_payload(build_raw_card_payload(card, force_closed=True))

            done_payload = sorted(done_cards, key=lambda item: item["number"])

            columns_payload = []
            for col in columns_sorted:
                col_id = normalize_id(col.get("id", ""))
                normalized = str(col.get("name", "")).strip().lower()
                columns_payload.append(
                    {
                        "id": col.get("id", ""),
                        "name": column_name_overrides.get(normalized, col.get("name", "")),
                        "cards": cards_by_column.get(col_id, []),
                        "count": len(cards_by_column.get(col_id, [])),
                    }
                )

            untriaged_sorted = sorted(untriaged, key=lambda item: item["number"])
            columns_payload.insert(
                0,
                {
                    "id": "untriaged",
                    "name": "Investigate",
                    "cards": untriaged_sorted,
                    "count": len(untriaged_sorted),
                },
            )

            return columns_payload, done_payload

        try:
            columns_payload, done_payload = await asyncio.to_thread(fetch_board)
            self.roadmap_columns = columns_payload
            self.roadmap_done_cards = done_payload
            self.roadmap_done_count = len(done_payload)
        except Exception as exc:  # pragma: no cover - surface user-friendly errors
            self.roadmap_error = str(exc)
        finally:
            self.roadmap_loading = False

    async def refresh_roadmap(self):
        """Force reload the roadmap data when the page is visited."""
        if self.roadmap_loading:
            return
        self.roadmap_columns = []
        self.roadmap_done_cards = []
        self.roadmap_done_count = 0
        self.roadmap_error = ""
        yield
        yield State.load_roadmap

    async def submit_contact_form(self, form_data: dict[str, Any]):
        """Send the contact form details via SMTP."""
        if self.contact_submission_inflight:
            return

        self.contact_error = ""
        self.contact_status = ""
        self.contact_email_error = ""
        self.contact_message_error = ""
        self.contact_submission_inflight = True
        yield

        cooldown_seconds = int(os.getenv("CONTACT_SUBMISSION_COOLDOWN_SECONDS", "30"))
        now = time.time()
        if self.contact_cooldown_remaining > 0:
            remaining = self.contact_cooldown_remaining
            self.contact_error = (
                f"Please wait {remaining} seconds before sending another message."
            )
            self.contact_submission_inflight = False
            return

        name = (form_data.get("name") or "").strip()
        email = (form_data.get("email") or self.contact_form_email or "").strip()
        organization = (form_data.get("organization") or "").strip()
        topic = (form_data.get("topic") or "").strip()
        message = (form_data.get("message") or self.contact_form_message or "").strip()

        if not email or not EMAIL_PATTERN.match(email):
            self.contact_email_error = "Enter a valid email address (example: name@domain.com)."

        if not message:
            self.contact_message_error = "Please include a message so we can help."

        if self.contact_email_error or self.contact_message_error:
            self.contact_error = "Please fix the highlighted fields below."
            self.contact_submission_inflight = False
            return

        subject_bits = [topic or "Foundation contact"]
        if name:
            subject_bits.append(name)
        elif email:
            subject_bits.append(email)
        subject = " - ".join(subject_bits)

        body_lines = []
        if name:
            body_lines.append(f"Name: {name}")
        if email:
            body_lines.append(f"Email: {email}")
        if organization:
            body_lines.append(f"Organization: {organization}")
        if topic:
            body_lines.append(f"Topic: {topic}")
        body_lines.append("")
        body_lines.append(message or "(No message provided)")
        body = "\n".join(body_lines)
        recipient = os.getenv("CONTACT_EMAIL_TO", "info@xian.technology").strip()
        sender = os.getenv("CONTACT_EMAIL_FROM", "").strip()
        if not sender:
            sender = os.getenv("SMTP_USERNAME", "").strip() or recipient

        try:
            await asyncio.to_thread(
                send_contact_email,
                subject,
                body,
                sender=sender,
                recipient=recipient,
                reply_to=email or None,
            )
        except Exception as exc:  # pragma: no cover - surface user-friendly errors
            self.contact_error = f"Message failed to send. Error: {exc}"
        else:
            self.contact_status = "Message sent. The foundation will follow up soon."
            self.contact_last_sent_at = now
            if cooldown_seconds > 0:
                self.contact_cooldown_remaining = cooldown_seconds
                yield State.run_contact_cooldown
            self.contact_form_email = ""
            self.contact_form_message = ""
            self.contact_form_key += 1
        finally:
            self.contact_submission_inflight = False

    @rx.event(background=True)
    async def run_contact_cooldown(self):
        """Count down without blocking other UI events."""
        while True:
            async with self:
                remaining = self.contact_cooldown_remaining
            if remaining <= 0:
                break
            await asyncio.sleep(1)
            async with self:
                self.contact_cooldown_remaining = max(0, self.contact_cooldown_remaining - 1)
            yield

    def set_contact_email(self, value: str):
        """Live-validate the email field as the user types."""
        email = value.strip()
        self.contact_form_email = value
        self.contact_status = ""
        self.contact_error = ""
        if not email:
            self.contact_email_error = "Email is required."
            return
        if not EMAIL_PATTERN.match(email):
            self.contact_email_error = "Enter a valid email address (example: name@domain.com)."
            return
        self.contact_email_error = ""

    def set_contact_message(self, value: str):
        """Live-validate the message field as the user types."""
        message = value.strip()
        self.contact_form_message = value
        self.contact_status = ""
        self.contact_error = ""
        if not message:
            self.contact_message_error = "Please include a message so we can help."
            return
        self.contact_message_error = ""

    def reset_contact_view(self):
        """Clear contact form UI state when visiting the page."""
        self.contact_status = ""
        self.contact_error = ""
        self.contact_email_error = ""
        self.contact_message_error = ""
        self.contact_form_email = ""
        self.contact_form_message = ""
        self.contact_form_key += 1

    async def command_palette_select_active(self):
        """Navigate to the currently selected item."""
        active = self.command_palette_active_action
        if not active["placeholder"]:
            yield State.close_command_palette
        yield rx.redirect(active["href"])

    @rx.var(cache=True, auto_deps=False, deps=["command_query"])
    def command_palette_actions(self) -> list[CommandAction]:
        """Return filtered actions for the command palette."""
        from ..search import SEARCH_ENTRIES

        query = self.command_query.strip().lower()
        if not query:
            return SEARCH_ENTRIES

        def matches(action: CommandAction) -> bool:
            haystack = " ".join(
                [
                    action.get("title", ""),
                    action.get("subtitle", ""),
                    " ".join(action.get("keywords", [])),
                    action.get("category", ""),
                ]
            ).lower()
            return query in haystack

        return [
            action
            for action in SEARCH_ENTRIES
            if matches(action)
        ]

    @rx.var
    def command_palette_empty(self) -> bool:
        """Determine if the palette has no search matches."""
        return len(self.command_palette_actions) == 0

    @rx.var
    def command_palette_sections(self) -> list[CommandSection]:
        """Flatten grouped actions into header + item sections."""
        sections: list[CommandSection] = []
        current_category = ""
        for action in self.command_palette_actions:
            category = action.get("category", "")
            if category != current_category:
                sections.append(
                    {
                        "type": "header",
                        "category": category,
                        "id": f"header-{category}",
                    }
                )
                current_category = category
            sections.append(
                {
                    "type": "item",
                    "category": category,
                    "id": action["id"],
                    "title": action["title"],
                    "subtitle": action["subtitle"],
                    "badge": action["badge"],
                    "href": action["href"],
                    "external": action["external"],
                    "keywords": action["keywords"],
                }
            )
        return sections

    @rx.var
    def command_palette_active_action(self) -> ActiveCommandInfo:
        """Return the currently highlighted action or a placeholder."""
        placeholder: ActiveCommandInfo = {
            "id": "palette-placeholder",
            "title": "Search the Xian Technology site",
            "subtitle": "Use keywords from any page — hero copy, stats, programs, or docs — to jump directly to the right section.",
            "category": "Hint",
            "badge": "Tip",
            "href": "#",
            "external": False,
            "keywords": [
                "Try 'deterministic python', 'research guild', or 'foundation contact'."
            ],
            "placeholder": True,
        }
        active_id = self.command_palette_active_id
        for action in self.command_palette_actions:
            if action["id"] == active_id:
                result: ActiveCommandInfo = {
                    **action,
                    "placeholder": False,
                }
                return result
        return placeholder

    @rx.var
    def has_command_palette_selection(self) -> bool:
        """Convenience flag for template logic."""
        return not self.command_palette_active_action["placeholder"]


__all__ = ["State"]
