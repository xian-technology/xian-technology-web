from typing import Any

import reflex as rx

from ..components.common import icon_watermark_hover_card, page_layout, section
from ..contact_guard import (
    MAX_MESSAGE_LENGTH,
    MAX_NAME_LENGTH,
    MAX_ORGANIZATION_LENGTH,
    MAX_TOPIC_LENGTH,
)
from ..state import State
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_HOVER,
    ACCENT_SOFT,
    BORDER_COLOR,
    PRIMARY_BG,
    SURFACE_BRIGHT,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

SEARCH_SECTIONS = [
    {
        "title": "Contact the Foundation",
        "subtitle": "Send partnership, support, or general inquiries to the Xian team.",
        "category": "About",
        "badge": "Page",
        "href": "/contact",
        "keywords": ["Contact", "Foundation", "Support", "Partnerships"],
    }
]

EMAIL_PATTERN = r"^(?=.{3,254}$)(?=.{1,64}@)[A-Za-z0-9](?:[A-Za-z0-9._%+-]{0,62}[A-Za-z0-9])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$"
ERROR_COLOR = rx.color_mode_cond(light="#dc2626", dark="#f87171")
ERROR_GLOW = rx.color_mode_cond(light="rgba(220, 38, 38, 0.25)", dark="rgba(248, 113, 113, 0.25)")



_FIELD_MAX_LENGTHS = {
    "name": MAX_NAME_LENGTH,
    "organization": MAX_ORGANIZATION_LENGTH,
    "topic": MAX_TOPIC_LENGTH,
}

def contact_page() -> rx.Component:
    """Contact page with message form."""

    def form_field(
        label: str,
        name: str,
        placeholder: str,
        *,
        field_type: str = "text",
        required: bool = False,
        pattern: str | None = None,
        title: str | None = None,
        error: rx.Var | str = "",
        value: rx.Var | str | None = None,
        on_change: Any | None = None,
    ) -> rx.Component:
        has_error = error != ""
        placeholder_color = rx.color_mode_cond(light="#6b7280", dark="#9ca3af")
        input_props = {
            "name": name,
            "id": name,
            "max_length": _FIELD_MAX_LENGTHS.get(name, 254),
            "placeholder": placeholder,
            "type": field_type,
            "required": required,
            "pattern": pattern,
            "title": title,
            "width": "100%",
            "height": "3.5rem",
            "padding": "0.9rem 1rem",
            "border": rx.cond(has_error, f"1px solid {ERROR_COLOR}", f"1px solid {BORDER_COLOR}"),
            "border_radius": "10px",
            "background": SURFACE_BRIGHT,
            "color": TEXT_PRIMARY,
            "font_size": "1rem",
            "line_height": "1.6",
            "style": {"& input::placeholder": {"color": placeholder_color, "opacity": "1"}},
            "_focus": {
                "borderColor": rx.cond(has_error, ERROR_COLOR, ACCENT),
                "outline": "none",
                "boxShadow": rx.cond(has_error, f"0 0 0 3px {ERROR_GLOW}", f"0 0 0 3px {ACCENT_GLOW}"),
            },
            "_focus_within": {
                "borderColor": rx.cond(has_error, ERROR_COLOR, ACCENT),
                "outline": "none",
                "boxShadow": rx.cond(has_error, f"0 0 0 3px {ERROR_GLOW}", f"0 0 0 3px {ACCENT_GLOW}"),
            },
        }
        if value is not None:
            input_props["value"] = value
        if on_change is not None:
            input_props["on_change"] = on_change

        return rx.vstack(
            rx.text(
                f"{label}{' *' if required else ''}",
                size="2",
                weight="medium",
                color=TEXT_MUTED,
            ),
            rx.input(**input_props),
            rx.cond(
                has_error,
                rx.text(error, size="2", color=ERROR_COLOR),
                rx.box(),
            ),
            spacing="2",
            align_items="start",
            width="100%",
        )

    def message_field(
        *,
        error: rx.Var | str = "",
        value: rx.Var | str | None = None,
        on_change: Any | None = None,
    ) -> rx.Component:
        has_error = error != ""
        placeholder_color = rx.color_mode_cond(light="#6b7280", dark="#9ca3af")
        text_area_props = {
            "name": "message",
            "id": "message",
            "max_length": MAX_MESSAGE_LENGTH,
            "placeholder": "Tell us what you are working on, and how we can help.",
            "required": True,
            "rows": "6",
            "resize": "vertical",
            "width": "100%",
            "min_height": "220px",
            "padding": "0.9rem 1rem",
            "border": rx.cond(has_error, f"1px solid {ERROR_COLOR}", f"1px solid {BORDER_COLOR}"),
            "border_radius": "10px",
            "background": SURFACE_BRIGHT,
            "color": TEXT_PRIMARY,
            "font_size": "1rem",
            "line_height": "1.6",
            "style": {"& textarea::placeholder": {"color": placeholder_color, "opacity": "1"}},
            "_focus": {
                "borderColor": rx.cond(has_error, ERROR_COLOR, ACCENT),
                "outline": "none",
                "boxShadow": rx.cond(has_error, f"0 0 0 3px {ERROR_GLOW}", f"0 0 0 3px {ACCENT_GLOW}"),
            },
            "_focus_within": {
                "borderColor": rx.cond(has_error, ERROR_COLOR, ACCENT),
                "outline": "none",
                "boxShadow": rx.cond(has_error, f"0 0 0 3px {ERROR_GLOW}", f"0 0 0 3px {ACCENT_GLOW}"),
            },
        }
        if value is not None:
            text_area_props["value"] = value
        if on_change is not None:
            text_area_props["on_change"] = on_change

        return rx.vstack(
            rx.text("Message *", size="2", weight="medium", color=TEXT_MUTED),
            rx.text_area(**text_area_props),
            rx.cond(
                has_error,
                rx.text(error, size="2", color=ERROR_COLOR),
                rx.box(),
            ),
            spacing="2",
            align_items="start",
            width="100%",
        )

    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("CONTACT", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Contact the Foundation",
                    size="8",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    line_height="1.2",
                ),
                rx.text(
                    "Send us a note about partnerships, support, or questions about the Xian stack.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    max_width="900px",
                ),
                rx.cond(
                    State.contact_error != "",
                    rx.callout.root(
                        rx.callout.icon(rx.icon(tag="triangle_alert")),
                        rx.callout.text(State.contact_error),
                        color_scheme="red",
                        role="alert",
                        size="2",
                        width="100%",
                    ),
                    rx.cond(
                        State.contact_status != "",
                        rx.callout.root(
                            rx.callout.icon(rx.icon(tag="check")),
                            rx.callout.text(State.contact_status),
                            color_scheme="green",
                            role="status",
                            size="2",
                            width="100%",
                        ),
                        rx.box(),
                    ),
                ),
                icon_watermark_hover_card(
                    rx.form(
                        rx.vstack(
                            rx.grid(
                                form_field("Full name", "name", "Jane Doe"),
                                form_field(
                                    "Email address",
                                    "email",
                                    "jane@company.com",
                                    field_type="email",
                                    required=True,
                                    pattern=EMAIL_PATTERN,
                                    title="Enter a valid email address (example: name@domain.com).",
                                    error=State.contact_email_error,
                                    value=State.contact_form_email,
                                    on_change=State.set_contact_email,
                                ),
                                columns={
                                    "base": "repeat(1, minmax(0, 1fr))",
                                    "md": "repeat(2, minmax(0, 1fr))",
                                },
                                spacing="4",
                                width="100%",
                            ),
                            rx.grid(
                                form_field("Organization", "organization", "Company or DAO"),
                                form_field("Topic", "topic", "Partnership, support, or other"),
                                columns={
                                    "base": "repeat(1, minmax(0, 1fr))",
                                    "md": "repeat(2, minmax(0, 1fr))",
                                },
                                spacing="4",
                                width="100%",
                            ),
                            message_field(
                                error=State.contact_message_error,
                                value=State.contact_form_message,
                                on_change=State.set_contact_message,
                            ),
                            rx.button(
                                rx.cond(
                                    State.contact_submission_inflight,
                                    "Sending...",
                                    rx.cond(
                                        State.contact_cooldown_remaining > 0,
                                        "Wait " + State.contact_cooldown_remaining.to_string() + "s...",
                                        "Send message",
                                    ),
                                ),
                                type="submit",
                                size="4",
                                background_color=ACCENT,
                                color=PRIMARY_BG,
                                border_radius="10px",
                                padding="1.1rem 1.6rem",
                                width="100%",
                                cursor="pointer",
                                disabled=State.contact_submission_inflight
                                | (State.contact_cooldown_remaining > 0),
                                _hover={"backgroundColor": ACCENT_HOVER},
                                _disabled={"opacity": "0.65", "cursor": "not-allowed"},
                            ),
                            spacing="4",
                            align_items="start",
                            width="100%",
                        ),
                        on_submit=State.submit_contact_form,
                        reset_on_submit=False,
                        key=State.contact_form_key,
                    ),
                    icon="mail",
                    padding="3rem",
                ),
                spacing="6",
                align_items="start",
                width="100%",
            ),
            on_mount=State.reset_contact_view,
        )
    )


__all__ = ["contact_page"]
