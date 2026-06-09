import re
from hashlib import md5
from typing import Any, Optional, TypedDict

import reflex as rx

from ..data import NAV_LINKS
from ..state import State
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    BORDER_COLOR,
    CODE_BG,
    MAX_CONTENT_WIDTH,
    PRIMARY_BG,
    SURFACE,
    SURFACE_BRIGHT,
    SURFACE_HOVER,
    TEXT_MUTED,
    TEXT_PRIMARY,
    TOP_GRADIENT,
)

NAV_DROPDOWN_LABELS = [link["label"] for link in NAV_LINKS if link.get("children")]
HEADER_CONTROL_HEIGHT = "2.6rem"
HEADER_CONTROL_RADIUS = "12px"


class SectionActionLink(TypedDict, total=False):
    """Config for a compact section action link."""

    label: str
    href: str
    icon: str
    is_external: bool
    show_label: bool
    show_label_from: str
    icon_size: int
    aria_label: str


def _header_control_style() -> dict[str, Any]:
    """Shared visual system for top-right header controls."""
    return {
        "variant": "ghost",
        "cursor": "pointer",
        "flex_shrink": "0",
        "height": HEADER_CONTROL_HEIGHT,
        "border_radius": HEADER_CONTROL_RADIUS,
        "border": f"1px solid {BORDER_COLOR}",
        "background_color": rx.color_mode_cond(
            light="rgba(255, 255, 255, 0.65)",
            dark="rgba(12, 18, 26, 0.6)",
        ),
        "backdrop_filter": "blur(16px)",
        "color": TEXT_PRIMARY,
        "transition": "border-color 0.2s ease, color 0.2s ease, transform 0.15s ease",
        "_hover": {
            "borderColor": ACCENT,
            "color": ACCENT,
        },
        "_active": {"transform": "scale(0.96)"},
        "_focus_visible": {
            "outline": f"2px solid {ACCENT}",
            "outlineOffset": "2px",
        },
    }


def _nav_has_dropdown(label_var: rx.Var) -> rx.Var:
    """Return True if the hovered label has dropdown children."""
    active: rx.Var | bool = False
    for label in NAV_DROPDOWN_LABELS:
        active = rx.cond(label_var == label, True, active)
    return active


def _interactive_link_style(*, radius: str = "10px") -> dict[str, Any]:
    """Shared tap/focus behavior for anchor-like controls."""
    return {
        "style": {"WebkitTapHighlightColor": "transparent"},
        "_focus": {"outline": "none"},
        "_focus_visible": {
            "outline": "none",
            "backgroundColor": ACCENT_SOFT,
            "borderRadius": radius,
        },
    }


def section(*children: rx.Component, **kwargs) -> rx.Component:
    """Wrap content in a centered section with generous spacing."""
    identifier = kwargs.pop("id", None)
    kwargs.setdefault("width", "100%")
    kwargs.setdefault("max_width", MAX_CONTENT_WIDTH)
    kwargs.setdefault("margin", "0 auto")
    kwargs.setdefault("padding_left", rx.breakpoints(initial="0.9rem", md="1.5rem", lg="2rem"))
    kwargs.setdefault("padding_right", rx.breakpoints(initial="0.9rem", md="1.5rem", lg="2rem"))
    kwargs.setdefault("padding_top", "2rem")
    kwargs.setdefault("padding_bottom", "2rem")
    return rx.box(*children, id=identifier, **kwargs)


def _anchor_id(value: str) -> str:
    """Create a URL-safe anchor id from a heading."""
    slug = value.lower().replace("&", "and")
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = slug.replace("_", "-")
    slug = re.sub(r"\s+", "-", slug).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug


def linked_heading(
    title: str,
    *,
    href: Optional[str] = None,
    anchor_id: Optional[str] = None,
    size: str = "6",
    icon_size: int = 18,
    scroll_margin_top: str = "2rem",
    **heading_kwargs: Any,
) -> rx.Component:
    """Heading with a hover-revealed anchor link icon."""
    anchor = anchor_id or _anchor_id(title)
    link_href = href or f"#{anchor}"
    return rx.link(
        rx.heading(title, size=size, **heading_kwargs),
        rx.icon(tag="link", size=icon_size, class_name="anchor-icon"),
        href=link_href,
        id=anchor,
        aria_label=f"Link to {title}",
        display="inline-flex",
        align_items="center",
        gap="0.5rem",
        text_decoration="none",
        color="inherit",
        style={
            "scrollMarginTop": scroll_margin_top,
            "& .anchor-icon": {
                "opacity": "0",
                "transform": "translateY(1px)",
                "transition": "opacity 0.2s ease, transform 0.2s ease, color 0.2s ease",
                "color": TEXT_MUTED,
            },
            "&:hover .anchor-icon": {
                "opacity": "1",
                "transform": "translateY(0)",
                "color": ACCENT,
            },
            "&:focus-visible .anchor-icon": {
                "opacity": "1",
                "transform": "translateY(0)",
                "color": ACCENT,
            },
        },
    )


def subsection(title: str, *children: rx.Component, **kwargs) -> rx.Component:
    """Section block with consistent spacing and a title."""
    spacing = kwargs.pop("spacing", "3")
    margin_top = kwargs.pop("margin_top", "1.5rem")
    heading_size = kwargs.pop("heading_size", "5")
    heading_id = kwargs.pop("id", None)
    heading_href = kwargs.pop("href", None)
    return rx.vstack(
        linked_heading(
            title,
            size=heading_size,
            color=TEXT_PRIMARY,
            weight="bold",
            href=heading_href,
            anchor_id=heading_id,
            scroll_margin_top="0.5rem",
        ),
        *children,
        spacing=spacing,
        align_items="start",
        width="100%",
        min_width="0",
        margin_top=margin_top,
        **kwargs,
    )


def inline_code(text: str) -> rx.Component:
    """Inline code token with shared theme styling."""
    return rx.el.code(
        text,
        style={
            "fontFamily": "'SF Mono', 'Monaco', monospace",
            "fontSize": "0.9em",
            "background": CODE_BG,
            "border": f"1px solid {BORDER_COLOR}",
            "borderRadius": "6px",
            "padding": "0.08rem 0.35rem",
            "color": TEXT_PRIMARY,
        },
    )


def text_with_inline_code(text: str, **text_kwargs: Any) -> rx.Component:
    """Render `backticked` segments inside text as inline code."""
    tokens = re.split(r"(`[^`]+`)", text)
    parts: list[Any] = []
    for token in tokens:
        if not token:
            continue
        if token.startswith("`") and token.endswith("`"):
            parts.append(inline_code(token[1:-1]))
        else:
            parts.append(token)
    return rx.text(*parts, **text_kwargs)


def section_action_links(
    links: list[SectionActionLink],
    *,
    spacing: str = "4",
    align_items: str = "center",
    text_size: str = "3",
) -> rx.Component:
    """Render compact icon/action links for section headers.

    Each link can define label/icon/url and responsive label visibility.
    """

    def action_link(link: SectionActionLink) -> rx.Component:
        label = link["label"]
        icon = link.get("icon", "link")
        is_external = link.get("is_external", True)
        show_label = link.get("show_label", True)
        show_label_from = link.get("show_label_from", "md")

        link_children: list[rx.Component] = [rx.icon(tag=icon, size=link.get("icon_size", 18))]
        if show_label:
            label_display: Any = "inline"
            if show_label_from != "base":
                label_display = rx.breakpoints(initial="none", **{show_label_from: "inline"})
            link_children.append(rx.text(label, size=text_size, display=label_display))

        return rx.link(
            rx.hstack(
                *link_children,
                spacing="2",
                align_items="center",
            ),
            href=link["href"],
            is_external=is_external,
            color=TEXT_MUTED,
            _hover={"color": ACCENT},
            aria_label=link.get("aria_label", label),
        )

    return rx.hstack(
        *[action_link(link) for link in links],
        spacing=spacing,
        align_items=align_items,
    )


def section_panel(header: rx.Component, *children: rx.Component, **kwargs) -> rx.Component:
    """Highlight a page section with a header band and consistent spacing."""
    header_padding = kwargs.pop(
        "header_padding",
        rx.breakpoints(
            initial="1rem 1rem 0.9rem 1rem",
            md="1.75rem 1.75rem 1.25rem 1.75rem",
            lg="2.5rem 2.5rem 1.75rem 2.5rem",
        ),
    )
    body_padding = kwargs.pop(
        "body_padding",
        rx.breakpoints(
            initial="1rem",
            md="1.35rem 1.75rem 1.75rem 1.75rem",
            lg="2rem 2.5rem 2.5rem 2.5rem",
        ),
    )
    body_spacing = kwargs.pop("body_spacing", "4")
    header_background = rx.color_mode_cond(
        light="linear-gradient(180deg, rgba(80, 177, 101, 0.18) 0%, rgba(248, 249, 250, 0) 100%)",
        dark="linear-gradient(180deg, rgba(80, 177, 101, 0.22) 0%, rgba(15, 20, 28, 0) 100%)",
    )
    return rx.box(
        rx.box(
            header,
            padding=header_padding,
            background=header_background,
            width="100%",
            box_sizing="border-box",
        ),
        rx.box(
            rx.vstack(*children, spacing=body_spacing, align_items="start", width="100%"),
            padding=body_padding,
            width="100%",
            box_sizing="border-box",
        ),
        background=SURFACE,
        border=f"1px solid {BORDER_COLOR}",
        border_radius="0 0 16px 16px",
        overflow="hidden",
        width="100%",
        **kwargs,
    )


def theme_toggle() -> rx.Component:
    """Minimal theme toggle with smooth icon swap."""
    return rx.button(
        rx.box(
            rx.icon(
                tag="sun",
                size=18,
                color="currentColor",
                position="absolute",
                transition="opacity 0.28s ease, transform 0.28s ease",
                opacity=rx.color_mode_cond(light="1", dark="0"),
                transform=rx.color_mode_cond(light="scale(1) rotate(0deg)", dark="scale(0.85) rotate(-20deg)"),
                pointer_events="none",
            ),
            rx.icon(
                tag="moon",
                size=18,
                color="currentColor",
                position="absolute",
                transition="opacity 0.28s ease, transform 0.28s ease",
                opacity=rx.color_mode_cond(light="0", dark="1"),
                transform=rx.color_mode_cond(light="scale(0.85) rotate(20deg)", dark="scale(1) rotate(0deg)"),
                pointer_events="none",
            ),
            position="relative",
            width="1.5rem",
            height="1.5rem",
            display="inline-flex",
            align_items="center",
            justify_content="center",
        ),
        on_click=rx.toggle_color_mode,
        aria_label="Toggle light and dark theme",
        padding="0",
        min_width=HEADER_CONTROL_HEIGHT,
        width=HEADER_CONTROL_HEIGHT,
        display="inline-flex",
        align_items="center",
        justify_content="center",
        **_header_control_style(),
    )


def nav_link(link: dict[str, str], extra: Optional[rx.Component] = None) -> rx.Component:
    """Navigation link with consistent spacing."""
    return rx.link(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        link["label"],
                        size="3",
                        weight="medium",
                        color=TEXT_MUTED,
                    ),
                    extra if extra is not None else rx.box(),
                    align_items="center",
                    gap="0.35rem",
                ),
                rx.box(
                    bg=ACCENT,
                    height="2px",
                    width=rx.cond(
                        State.nav_hover_label == link["label"],
                        "100%",
                        "0%",
                    ),
                    transition="width 0.2s ease",
                    border_radius="999px",
                ),
                spacing="1",
                align_items="start",
            ),
            padding="0.35rem 0",
        ),
        href=link["href"],
        padding="0.35rem 0.1rem",
        transition="all 0.2s ease",
        display="inline-flex",
        align_items="center",
        gap="0.35rem",
        _hover={
            "textDecoration": "none",
            "color": ACCENT,
        },
        **_interactive_link_style(radius="8px"),
    )


def nav_label(link: dict[str, str], extra: Optional[rx.Component] = None) -> rx.Component:
    """Navigation label for dropdown triggers (non-clickable)."""
    return rx.box(
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        link["label"],
                        size="3",
                        weight="medium",
                        color=TEXT_MUTED,
                    ),
                    extra if extra is not None else rx.box(),
                    align_items="center",
                    gap="0.35rem",
                ),
                rx.box(
                    bg=ACCENT,
                    height="2px",
                    width=rx.cond(
                        State.nav_hover_label == link["label"],
                        "100%",
                        "0%",
                    ),
                    transition="width 0.2s ease",
                    border_radius="999px",
                ),
                spacing="1",
                align_items="start",
            ),
            padding="0.35rem 0",
        ),
        padding="0.35rem 0.1rem",
        transition="all 0.2s ease",
        display="inline-flex",
        align_items="center",
        gap="0.35rem",
        cursor="pointer",
        role="button",
        tab_index=0,
        _hover={
            "textDecoration": "none",
            "color": ACCENT,
        },
    )


def nav_item(link: dict[str, Any]) -> rx.Component:
    """Navigation item with hover tracking for mega menu."""
    return rx.box(
        nav_label(link) if link.get("children") else nav_link(link),
        on_mouse_enter=State.set_nav_hover(link["label"]),
        on_focus=State.set_nav_hover(link["label"]),
        display="inline-flex",
    )


def _submenu_item(child: dict) -> rx.Component:
    """Render a single submenu item, optionally highlighted with accent gradient."""
    highlighted = child.get("highlighted", False)

    # Normal state: green-to-green gradient (light green → darker green)
    light_normal_gradient = "linear-gradient(to right, rgba(0, 179, 92, 0.12) 0%, rgba(0, 179, 92, 0.25) 100%)"
    dark_normal_gradient = "linear-gradient(to right, rgba(0, 255, 136, 0.10) 0%, rgba(0, 255, 136, 0.20) 100%)"

    # Hover state: surface color → green gradient
    light_hover_gradient = "linear-gradient(to right, rgba(255, 255, 255, 0.95) 40%, rgba(0, 179, 92, 0.15) 100%)"
    dark_hover_gradient = "linear-gradient(to right, rgba(25, 35, 48, 0.95) 40%, rgba(0, 255, 136, 0.12) 100%)"

    base_props = {
        "transition": "transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease, color 0.2s ease",
        "display": "block",
    }
    if highlighted:
        base_props["background_image"] = rx.color_mode_cond(
            light=light_normal_gradient,
            dark=dark_normal_gradient,
        )

    # Hover styles
    if highlighted:
        hover_style = {
            "textDecoration": "none",
            "color": ACCENT,
            "backgroundImage": rx.color_mode_cond(
                light=light_hover_gradient,
                dark=dark_hover_gradient,
            ),
            "boxShadow": "0 12px 32px rgba(0,0,0,0.16)",
        }
    else:
        hover_style = {
            "textDecoration": "none",
            "color": ACCENT,
            "background": SURFACE_BRIGHT,
            "boxShadow": "0 12px 32px rgba(0,0,0,0.16)",
        }

    return rx.link(
        rx.box(
            rx.text(child["label"], size="1", weight="bold", color=TEXT_PRIMARY),
            rx.text(child["description"], size="2", color=TEXT_MUTED, line_height="1.5"),
            spacing="1",
            align_items="start",
        ),
        href=child["href"],
        _hover=hover_style,
        padding="0.85rem 0.95rem",
        border_radius="10px",
        width="100%",
        **base_props,
    )


def submenu_children(label: str) -> rx.Component:
    """Render submenu content for a hovered label."""
    groups: list[rx.Component] = []
    for link in NAV_LINKS:
        children = link.get("children")
        if not children:
            continue
        if link["label"] == "Developers":
            highlighted = [child for child in children if child.get("highlighted")]
            regular = [child for child in children if not child.get("highlighted")]
            content = rx.vstack(
                rx.grid(
                    rx.vstack(
                        rx.text("Highlighted", size="2", weight="bold", color=TEXT_MUTED, letter_spacing="0.08em"),
                        rx.vstack(
                            *[_submenu_item(child) for child in highlighted],
                            spacing="3",
                            align_items="start",
                            width="100%",
                        ),
                        spacing="3",
                        align_items="start",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Developers", size="2", weight="bold", color=TEXT_MUTED, letter_spacing="0.08em"),
                        rx.grid(
                            *[_submenu_item(child) for child in regular],
                            columns={
                                "initial": "repeat(1, minmax(0, 1fr))",
                                "md": "repeat(2, minmax(0, 1fr))",
                            },
                            spacing="3",
                            width="100%",
                        ),
                        spacing="3",
                        align_items="start",
                        width="100%",
                    ),
                    columns={
                        "initial": "repeat(1, minmax(0, 1fr))",
                        "md": "minmax(0, 1fr) minmax(0, 2fr)",
                    },
                    spacing="4",
                    width="100%",
                ),
                spacing="3",
                align_items="start",
                width="100%",
            )
        else:
            content = rx.vstack(
                rx.text(link["label"], size="2", weight="bold", color=TEXT_MUTED, letter_spacing="0.08em"),
                rx.grid(
                    *[_submenu_item(child) for child in children],
                    columns={
                        "initial": "repeat(1, minmax(0, 1fr))",
                        "md": "repeat(3, minmax(0, 1fr))",
                    },
                    spacing="3",
                    width="100%",
                ),
                spacing="3",
                align_items="start",
            )
        groups.append(
            rx.cond(
                State.nav_hover_label == link["label"],
                content,
                rx.box(),
            )
        )
    return rx.fragment(*groups)


def command_palette_button() -> rx.Component:
    """Compact trigger for the global command palette."""
    return rx.button(
        rx.hstack(
            rx.icon(tag="search", size=16, color="currentColor"),
            rx.text(
                "Search",
                size="2",
                color="currentColor",
                opacity="0.86",
                display=rx.breakpoints(initial="none", md="inline", lg="none"),
            ),
            rx.text(
                "Search the site",
                size="2",
                color="currentColor",
                opacity="0.86",
                display=rx.breakpoints(initial="none", lg="inline"),
            ),
            rx.box(
                "⌘K",
                font_size="0.75rem",
                color="currentColor",
                padding="0.1rem 0.4rem",
                border="1px solid currentColor",
                border_radius="0.4rem",
                opacity="0.72",
                display=rx.breakpoints(initial="none", lg="block"),
            ),
            align_items="center",
            gap="0.5rem",
        ),
        on_click=State.open_command_palette,
        padding=rx.breakpoints(initial="0", md="0 0.7rem", lg="0 0.85rem"),
        width=rx.breakpoints(initial=HEADER_CONTROL_HEIGHT, md="auto"),
        min_width=rx.breakpoints(initial=HEADER_CONTROL_HEIGHT, md="0"),
        justify_content=rx.breakpoints(initial="center", md="flex-start"),
        **_header_control_style(),
    )


def _mobile_nav_item(link: dict[str, Any]) -> rx.Component:
    """Polished mobile nav row with optional child links."""
    children = link.get("children", [])
    has_children = bool(children)
    return rx.box(
        rx.link(
            rx.hstack(
                rx.text(link["label"], size="4", weight="bold", color=TEXT_PRIMARY),
                rx.cond(
                    has_children,
                    rx.text(
                        "Section",
                        size="1",
                        color=ACCENT,
                        letter_spacing="0.08em",
                        text_transform="uppercase",
                    ),
                    rx.icon(tag="arrow_up_right", size=14, color=TEXT_MUTED),
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),
            href=link["href"],
            display="block",
            width="100%",
            _hover={"textDecoration": "none", "color": ACCENT},
            on_click=State.close_mobile_nav,
            **_interactive_link_style(radius="10px"),
        ),
        rx.cond(
            has_children,
            rx.vstack(
                *[
                    rx.link(
                        rx.vstack(
                            rx.hstack(
                                rx.text(child["label"], size="2", weight="medium", color=TEXT_PRIMARY),
                                rx.icon(tag="arrow_up_right", size=14, color=TEXT_MUTED),
                                justify="between",
                                align_items="center",
                                width="100%",
                            ),
                            rx.text(
                                child["description"],
                                size="1",
                                color=TEXT_MUTED,
                                line_height="1.45",
                            ),
                            spacing="1",
                            align_items="start",
                            width="100%",
                        ),
                        href=child["href"],
                        width="100%",
                        display="block",
                        padding="0.62rem 0.72rem",
                        border=f"1px solid {BORDER_COLOR}",
                        border_radius="10px",
                        background=rx.color_mode_cond(
                            light="rgba(255, 255, 255, 0.82)",
                            dark="rgba(25, 35, 48, 0.42)",
                        ),
                        _hover={
                            "textDecoration": "none",
                            "color": ACCENT,
                            "borderColor": ACCENT,
                            "background": SURFACE_BRIGHT,
                        },
                        transition="all 0.2s ease",
                        on_click=State.close_mobile_nav,
                        **_interactive_link_style(radius="10px"),
                    )
                    for child in children
                ],
                spacing="2",
                align_items="start",
                width="100%",
                margin_top="0.65rem",
            ),
            rx.box(),
        ),
        padding="0.85rem",
        border=f"1px solid {BORDER_COLOR}",
        border_radius="14px",
        background=rx.color_mode_cond(
            light="rgba(255, 255, 255, 0.72)",
            dark="rgba(12, 18, 26, 0.45)",
        ),
        width="100%",
    )


def mobile_nav_panel() -> rx.Component:
    """Slide-down mobile navigation with polished grouped cards."""
    return rx.cond(
        State.mobile_nav_open,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.text(
                        "Explore",
                        size="1",
                        weight="medium",
                        color=TEXT_MUTED,
                        letter_spacing="0.08em",
                        text_transform="uppercase",
                    ),
                    rx.box(height="1px", flex="1", background=BORDER_COLOR),
                    align_items="center",
                    width="100%",
                    gap="0.65rem",
                ),
                *[_mobile_nav_item(link) for link in NAV_LINKS],
                spacing="3",
                align_items="start",
                width="100%",
            ),
            background=rx.color_mode_cond(
                light="rgba(248, 249, 250, 0.98)",
                dark="rgba(15, 20, 28, 0.98)",
            ),
            position="absolute",
            top="100%",
            left="0",
            right="0",
            z_index="90",
            border=f"1px solid {BORDER_COLOR}",
            border_top="none",
            border_radius="0 0 16px 16px",
            padding="0.9rem 1rem 1.1rem",
            box_shadow=rx.color_mode_cond(
                light="0 18px 34px rgba(15, 23, 42, 0.12)",
                dark="0 22px 36px rgba(0, 0, 0, 0.42)",
            ),
            backdrop_filter="blur(10px)",
            max_height="70vh",
            overflow_y="auto",
            display=rx.breakpoints(initial="block", lg="none"),
        ),
        rx.box(),
    )


def nav_bar() -> rx.Component:
    """Professional navigation bar."""
    border_color = rx.color_mode_cond(
        light="1px solid rgba(15, 23, 42, 0.08)",
        dark="1px solid rgba(255, 255, 255, 0.12)",
    )
    base_shadow = rx.color_mode_cond(
        light="0 1px 20px rgba(15, 23, 42, 0.08)",
        dark="0 1px 20px rgba(0, 0, 0, 0.35)",
    )
    dropdown_active = _nav_has_dropdown(State.nav_hover_label)
    box_shadow = rx.cond(dropdown_active, "none", base_shadow)
    filter_shadow = "none"
    return rx.box(
        # Background layer for the nav surface (kept separate to avoid stacking context issues)
        rx.box(
            position="absolute",
            top="0",
            left="0",
            right="0",
            bottom="0",
            background_color=SURFACE,
            z_index="-1",
            transition="background-color 0.3s ease",
        ),
        rx.box(
            rx.box(
                rx.flex(
                    rx.link(
                        rx.flex(
                            rx.image(
                                src="/xian.jpg",
                                alt="Xian Technology Logo",
                                width=rx.breakpoints(initial="2.35rem", md="3rem"),
                                height=rx.breakpoints(initial="2.35rem", md="3rem"),
                                border_radius="8px",
                                object_fit="cover",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Xian Technology",
                                    weight="bold",
                                    size=rx.breakpoints(initial="3", md="4"),
                                    color=TEXT_PRIMARY,
                                ),
                                rx.text(
                                    "Python-native contracting",
                                    size="2",
                                    color=TEXT_MUTED,
                                    display=rx.breakpoints(initial="none", md="block"),
                                ),
                                align_items="start",
                                spacing="0",
                            ),
                            gap=rx.breakpoints(initial="0.6rem", md="1rem"),
                            align_items="center",
                        ),
                        href="/",
                        _hover={"textDecoration": "none"},
                        **_interactive_link_style(radius="12px"),
                    ),
                    rx.flex(
                        *[nav_item(link) for link in NAV_LINKS],
                        gap="0.75rem",
                        justify="center",
                        align_items="center",
                        flex="1",
                        display=rx.breakpoints(initial="none", lg="flex"),
                    ),
                    rx.flex(
                        command_palette_button(),
                        theme_toggle(),
                        rx.button(
                            rx.icon(tag="menu", size=21),
                            on_click=State.toggle_mobile_nav,
                            display=rx.breakpoints(initial="flex", lg="none"),
                            padding="0",
                            width=HEADER_CONTROL_HEIGHT,
                            min_width=HEADER_CONTROL_HEIGHT,
                            align_items="center",
                            justify_content="center",
                            **_header_control_style(),
                        ),
                        spacing="6",
                        align_items="center",
                        flex_shrink="0",
                    ),
                    align_items="center",
                    width="100%",
                    gap=rx.breakpoints(initial="0.65rem", md="1.25rem"),
                    justify="between",
                ),
                max_width=MAX_CONTENT_WIDTH,
                margin="0 auto",
                padding=rx.breakpoints(initial="0 1rem", md="0 1.5rem", lg="0 2rem"),
            ),
        ),
        rx.box(
            rx.box(
                rx.box(
                    submenu_children(State.nav_hover_label),
                    padding="1.5rem 2rem",
                    max_width=MAX_CONTENT_WIDTH,
                    width="100%",
                    margin="0 auto",
                ),
                position="relative",
                background=SURFACE,
                border=f"1px solid {BORDER_COLOR}",
                border_top="none",
                border_radius="0px",
                box_shadow="none",
                width="100%",
                overflow="hidden",
                opacity=rx.cond(dropdown_active, "1", "0"),
                transform=rx.cond(dropdown_active, "translateY(0)", "translateY(6px)"),
                visibility=rx.cond(dropdown_active, "visible", "hidden"),
                transition="opacity 0.18s cubic-bezier(0.22, 0.61, 0.36, 1), transform 0.18s cubic-bezier(0.22, 0.61, 0.36, 1), visibility 0s",
                pointer_events=rx.cond(dropdown_active, "auto", "none"),
            ),
            position="absolute",
            top="100%",
            left="0",
            right="0",
            padding_top="0px",
            padding_left="0",
            padding_right="0",
            z_index="99",
            display=rx.breakpoints(initial="none", lg="block"),
        ),
        mobile_nav_panel(),
        position="sticky",
        top="0",
        z_index="100",
        border_bottom=rx.cond(
            dropdown_active,
            "1px solid transparent",
            rx.cond(State.mobile_nav_open, "1px solid transparent", border_color),
        ),
        padding="0.85rem 0",
        width="100%",
        on_mouse_leave=State.clear_nav_hover,
        filter=rx.breakpoints(initial="none", lg=filter_shadow),
        box_shadow=rx.breakpoints(initial="none", lg=box_shadow),
        transition="filter 0.18s ease, box-shadow 0.18s ease",
    )


def code_block(code: str) -> rx.Component:
    """Syntax-highlight friendly code block."""
    return rx.box(
        rx.text(
            code,
            font_family="'SF Mono', 'Monaco', 'Menlo', 'Courier New', monospace",
            size="2",
            color=rx.color_mode_cond(light="#1f2937", dark="#c9d1d9"),
            white_space="pre",
            line_height="1.6",
        ),
        background=CODE_BG,
        border=f"1px solid {BORDER_COLOR}",
        border_radius="10px",
        padding=rx.breakpoints(initial="1rem", md="1.25rem", lg="1.5rem"),
        overflow_x="auto",
        width="100%",
        transition="all 0.3s ease",
    )


def copyable_code_block(
    code: str,
    *,
    copied: rx.Var | bool | None = None,
    on_copy: Any = None,
    copy_key: str | None = None,
    language: str = "python",
    show_line_numbers: bool = True,
    wrap_long_lines: bool = False,
    copy_button_top: str = "0.8rem",
    copy_button_right: str = "0.95rem",
    block_margin_top: str = "0",
    copy_icon_size: int = 20,
    copy_button_padding: str = "0.4rem",
) -> rx.Component:
    """Code block with a persistent top-right copy control and copy feedback state."""
    resolved_copy_key = copy_key
    if resolved_copy_key is None:
        digest = md5(f"{language}:{code}".encode("utf-8"), usedforsecurity=False).hexdigest()[:16]
        resolved_copy_key = f"code-{digest}"

    resolved_copied = copied
    if resolved_copied is None:
        resolved_copied = State.copied_code_key == resolved_copy_key

    on_copy_event = on_copy if on_copy is not None else State.copy_code_with_feedback(code, resolved_copy_key)
    icon_size_px = f"{copy_icon_size}px"

    return rx.box(
        rx.code_block(
            code,
            language=language,
            show_line_numbers=show_line_numbers,
            wrap_long_lines=wrap_long_lines,
            custom_style={"overflowX": "auto", "margin": "0"},
            margin="0",
            width="100%",
        ),
        rx.button(
            rx.box(
                rx.icon(
                    tag="clipboard_copy",
                    size=copy_icon_size,
                    color="currentColor",
                    opacity=rx.cond(resolved_copied, "0", "1"),
                    transform=rx.cond(resolved_copied, "scale(0.85)", "scale(1)"),
                    transition="opacity 0.2s ease, transform 0.2s ease",
                    position="absolute",
                    top="0",
                    left="0",
                ),
                rx.icon(
                    tag="check",
                    size=copy_icon_size,
                    color="currentColor",
                    opacity=rx.cond(resolved_copied, "1", "0"),
                    transform=rx.cond(resolved_copied, "scale(1)", "scale(0.85)"),
                    transition="opacity 0.2s ease, transform 0.2s ease",
                    position="absolute",
                    top="0",
                    left="0",
                ),
                width=icon_size_px,
                height=icon_size_px,
                position="relative",
                display="inline-block",
            ),
            on_click=on_copy_event,
            variant="ghost",
            cursor="pointer",
            padding=copy_button_padding,
            min_width="unset",
            color=rx.cond(resolved_copied, ACCENT, TEXT_MUTED),
            background=rx.color_mode_cond(
                light="rgba(248, 249, 250, 0.92)",
                dark="rgba(15, 20, 28, 0.88)",
            ),
            border=f"1px solid {BORDER_COLOR}",
            border_radius="6px",
            _hover={
                "color": ACCENT,
                "border": f"1px solid {ACCENT_GLOW}",
                "background": rx.color_mode_cond(
                    light="rgba(241, 243, 245, 0.98)",
                    dark="rgba(20, 28, 38, 0.92)",
                ),
            },
            aria_label="Copy code",
            title="Copy code",
            position="absolute",
            top=copy_button_top,
            right=copy_button_right,
            z_index="2",
        ),
        style={
            "& > pre": {
                "margin": "0 !important",
            },
        },
        position="relative",
        margin_top=block_margin_top,
        width="100%",
    )


def hover_icon_chip(icon: str, *, size: int = 28) -> rx.Component:
    """Icon chip tuned for the card watermark hover effect."""
    return rx.box(
        rx.icon(tag=icon, size=size, color=ACCENT, class_name="wm-card-chip-icon"),
        class_name="wm-card-icon-chip",
    )


def icon_watermark_hover_card(
    *children: rx.Component,
    icon: str,
    show_watermark: bool = True,
    watermark_icon_size: int = 128,
    content_spacing: str = "3",
    content_align_items: str = "start",
    **kwargs: Any,
) -> rx.Component:
    """Reusable card shell with animated icon watermark hover effect."""
    gradient_overlay = rx.color_mode_cond(
        light="linear-gradient(135deg, rgba(80, 177, 101, 0.2), rgba(80, 177, 101, 0.08))",
        dark="linear-gradient(135deg, rgba(0, 255, 136, 0.14), rgba(0, 255, 136, 0.05))",
    )
    mesh_overlay = rx.color_mode_cond(
        light="linear-gradient(to right, rgba(128, 128, 128, 0.08) 1px, transparent 1px), linear-gradient(to bottom, rgba(128, 128, 128, 0.08) 1px, transparent 1px)",
        dark="linear-gradient(to right, rgba(255, 255, 255, 0.07) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.07) 1px, transparent 1px)",
    )
    blob_overlay = rx.color_mode_cond(
        light="radial-gradient(circle, rgba(80, 177, 101, 0.5) 0%, rgba(80, 177, 101, 0) 70%)",
        dark="radial-gradient(circle, rgba(0, 255, 136, 0.32) 0%, rgba(0, 255, 136, 0) 72%)",
    )
    watermark_icon_color = rx.color_mode_cond(
        light="#2e8c47",
        dark=ACCENT,
    )
    hover_mesh_opacity = rx.color_mode_cond(light="0.16", dark="0.1")
    hover_blob_opacity = rx.color_mode_cond(light="0.2", dark="0.2")
    hover_noise_opacity = rx.color_mode_cond(light="0.14", dark="0.2")
    hover_watermark_opacity = rx.color_mode_cond(light="0.13", dark="0.07")
    hover_shadow = rx.color_mode_cond(
        light="0 0 0 1px rgba(80, 177, 101, 0.16), 0 0 12px rgba(80, 177, 101, 0.12)",
        dark="0 0 0 1px rgba(0, 255, 136, 0.2), 0 0 12px rgba(0, 255, 136, 0.12)",
    )
    icon_chip_bg = rx.color_mode_cond(
        light="linear-gradient(135deg, #f9fafb, #f3f4f6)",
        dark="linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.05))",
    )
    icon_chip_border = rx.color_mode_cond(
        light="rgba(229, 231, 235, 0.95)",
        dark="rgba(255, 255, 255, 0.1)",
    )

    custom_hover = kwargs.pop("_hover", {})
    custom_style = kwargs.pop("style", {})

    padding_value = kwargs.pop("padding", None)
    if padding_value is None:
        resolved_padding = rx.breakpoints(initial="1rem", md="1.5rem", lg="2rem")
    elif isinstance(padding_value, str) and padding_value in {"0", "0rem", "0px"}:
        resolved_padding = padding_value
    elif isinstance(padding_value, str) and padding_value.endswith("rem") and " " not in padding_value:
        try:
            rem_value = float(padding_value[:-3])
            mobile_padding = max(0.85, round(rem_value * 0.62, 2))
            tablet_padding = max(1.0, round(rem_value * 0.8, 2))
            resolved_padding = rx.breakpoints(
                initial=f"{mobile_padding}rem",
                md=f"{tablet_padding}rem",
                lg=padding_value,
            )
        except ValueError:
            resolved_padding = padding_value
    else:
        resolved_padding = padding_value

    kwargs["padding"] = resolved_padding
    kwargs.setdefault("background", SURFACE)
    kwargs.setdefault("border", f"1px solid {BORDER_COLOR}")
    kwargs.setdefault("border_radius", "14px")
    kwargs.setdefault("height", "100%")
    kwargs.setdefault("width", "100%")
    kwargs.setdefault("display", "flex")
    kwargs.setdefault("flex_direction", "column")
    kwargs.setdefault("position", "relative")
    kwargs.setdefault("overflow", "hidden")
    kwargs.setdefault("transition", "all 0.5s ease")

    style = {
        "& .wm-card-content": {
            "position": "relative",
            "zIndex": "1",
        },
        "& .wm-card-gradient": {
            "position": "absolute",
            "inset": "0",
            "background": gradient_overlay,
            "opacity": "0",
            "transition": "opacity 0.5s ease",
            "pointerEvents": "none",
            "zIndex": "0",
        },
        "& .wm-card-mesh": {
            "position": "absolute",
            "inset": "0",
            "background": mesh_overlay,
            "backgroundSize": "20px 20px",
            "opacity": "0",
            "transition": "opacity 0.7s ease",
            "pointerEvents": "none",
            "zIndex": "0",
        },
        "& .wm-card-blob": {
            "position": "absolute",
            "right": "-5rem",
            "top": "-5rem",
            "height": "16rem",
            "width": "16rem",
            "borderRadius": "999px",
            "background": blob_overlay,
            "opacity": "0",
            "transform": "scale(1)",
            "filter": "blur(60px)",
            "transition": "opacity 0.7s ease, transform 0.7s ease",
            "pointerEvents": "none",
            "zIndex": "0",
        },
        "& .wm-card-noise": {
            "position": "absolute",
            "inset": "0",
            "opacity": "0",
            "transition": "opacity 0.5s ease",
            "backgroundImage": "url('https://grainy-gradients.vercel.app/noise.svg')",
            "mixBlendMode": "overlay",
            "filter": "brightness(1) contrast(1.5)",
            "pointerEvents": "none",
            "zIndex": "0",
        },
        "& .wm-card-watermark": {
            "position": "absolute",
            "bottom": "-1rem",
            "right": "-1rem",
            "opacity": "0",
            "transform": "rotate(12deg) scale(2.5)",
            "transition": "opacity 0.7s ease, transform 0.7s ease",
            "pointerEvents": "none",
            "zIndex": "0",
        },
        "& .wm-card-icon-chip": {
            "position": "relative",
            "display": "inline-flex",
            "alignItems": "center",
            "justifyContent": "center",
            "padding": "0.75rem",
            "borderRadius": "0.75rem",
            "background": icon_chip_bg,
            "border": f"1px solid {icon_chip_border}",
            "boxShadow": "0 1px 2px rgba(15, 23, 42, 0.08)",
            "transition": "transform 0.5s ease, border-color 0.35s ease",
        },
        "& .wm-card-chip-icon": {
            "transition": "color 0.3s ease",
        },
        "&:hover .wm-card-gradient": {
            "opacity": "1",
        },
        "&:hover .wm-card-mesh": {
            "opacity": hover_mesh_opacity,
        },
        "&:hover .wm-card-blob": {
            "opacity": hover_blob_opacity,
            "transform": "scale(1.25)",
        },
        "&:hover .wm-card-noise": {
            "opacity": hover_noise_opacity,
        },
        "&:hover .wm-card-watermark": {
            "opacity": hover_watermark_opacity,
            "transform": "rotate(0deg) scale(2.5)",
        },
        "&:hover .wm-card-icon-chip": {
            "transform": "scale(1.05)",
        },
    }
    style.update(custom_style)

    hover_style = {
        "borderColor": ACCENT,
        "backgroundColor": SURFACE_HOVER,
        "boxShadow": hover_shadow,
    }
    hover_style.update(custom_hover)

    watermark_layer: rx.Component = rx.box(
        rx.icon(tag=icon, size=watermark_icon_size, color=watermark_icon_color),
        class_name="wm-card-watermark",
    )
    if not show_watermark:
        watermark_layer = rx.box()

    return rx.box(
        rx.box(class_name="wm-card-gradient"),
        rx.box(class_name="wm-card-mesh"),
        rx.box(class_name="wm-card-blob"),
        rx.box(class_name="wm-card-noise"),
        watermark_layer,
        rx.vstack(
            *children,
            spacing=content_spacing,
            align_items=content_align_items,
            width="100%",
            class_name="wm-card-content",
        ),
        style=style,
        _hover=hover_style,
        **kwargs,
    )


def feature_card(title: str, description: str, icon: str) -> rx.Component:
    """Feature card with animated icon watermark hover affordance."""
    return icon_watermark_hover_card(
        hover_icon_chip(icon),
        rx.heading(title, size="5", color=TEXT_PRIMARY, weight="bold"),
        rx.text(
            description,
            size="3",
            color=TEXT_MUTED,
            line_height="1.7",
        ),
        icon=icon,
        padding="2.5rem",
        content_spacing="5",
    )



def command_palette() -> rx.Component:
    """Global command palette with CMD/CTRL + K shortcut."""

    def action_row(action: dict[str, Any]) -> rx.Component:
        arrow = rx.cond(
            action["external"],
            rx.icon(tag="arrow_up_right", size=18, color=TEXT_MUTED),
            rx.icon(tag="corner_down_left", size=18, color=TEXT_MUTED),
        )
        arrow_slot = rx.center(
            arrow,
            width="22px",
            height="22px",
            flex_shrink="0",
        )
        is_active = action["id"] == State.command_palette_active_id

        return rx.link(
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.text(action["title"], size="3", weight="medium", color=TEXT_PRIMARY),
                        rx.box(
                            action["badge"],
                            font_size="0.7rem",
                            color=ACCENT,
                            background=ACCENT_SOFT,
                            padding="0.1rem 0.45rem",
                            border_radius="6px",
                        ),
                        spacing="2",
                        align_items="center",
                        width="100%",
                        min_width="0",
                    ),
                    rx.text(
                        action["subtitle"],
                        size="2",
                        color=TEXT_MUTED,
                        width="100%",
                        style={
                            "whiteSpace": "nowrap",
                            "overflow": "hidden",
                            "textOverflow": "ellipsis",
                        },
                    ),
                    spacing="1",
                    align_items="start",
                    width="100%",
                    min_width="0",
                ),
                rx.spacer(),
                arrow_slot,
                align_items="center",
                width="100%",
            ),
            id=rx.cond(is_active, "palette-active-item", ""),
            href=action["href"],
            is_external=action["external"],
            on_click=State.close_command_palette,
            on_mouse_enter=State.set_command_palette_selection(action["id"]),
            padding="0.85rem 1rem",
            border_radius="12px",
            border=f"1px solid {BORDER_COLOR}",
            transition="all 0.2s ease",
            background=rx.cond(is_active, ACCENT_SOFT, "transparent"),
            border_color=rx.cond(is_active, ACCENT, BORDER_COLOR),
            _hover={
                "borderColor": ACCENT,
                "backgroundColor": ACCENT_SOFT,
                "textDecoration": "none",
            },
            width="100%",
        )

    def palette_list_entry(entry: dict[str, Any]) -> rx.Component:
        header = rx.box(
            rx.text(
                entry["category"],
                size="2",
                color=TEXT_MUTED,
                text_transform="uppercase",
                letter_spacing="0.2em",
            ),
            padding_top="0.5rem",
        )

        return rx.cond(
            entry["type"] == "header",
            header,
            action_row(entry),
        )

    return rx.fragment(
        rx.button(on_click=State.open_command_palette, id="command-palette-trigger", display="none"),
        rx.button(on_click=State.close_command_palette, id="command-palette-close", display="none"),
        rx.button(on_click=State.command_palette_move_up, id="command-palette-up", display="none"),
        rx.button(on_click=State.command_palette_move_down, id="command-palette-down", display="none"),
        rx.button(on_click=State.command_palette_select_active, id="command-palette-select", display="none"),
        rx.script(src="/js/command-palette.js"),
        rx.cond(
            State.command_palette_visible,
            rx.fragment(
                rx.center(
                    rx.box(
                        rx.vstack(
                            rx.text_field(
                                rx.text_field.slot(
                                    rx.button(
                                        "ESC",
                                        on_click=State.close_command_palette,
                                        size="1",
                                        variant="outline",
                                        color=TEXT_MUTED,
                                        border_color=BORDER_COLOR,
                                        background_color=rx.color_mode_cond(
                                            light="rgba(255, 255, 255, 0.7)",
                                            dark="rgba(12, 18, 26, 0.6)",
                                        ),
                                        padding="0.1rem 0.6rem",
                                        font_size="0.75rem",
                                        cursor="pointer",
                                        title="Close",
                                        _hover={
                                            "color": ACCENT,
                                            "borderColor": ACCENT,
                                        },
                                    ),
                                    side="right",
                                ),
                                value=State.command_query,
                                on_change=State.set_command_query,
                                placeholder='Try "deterministic python", "research guild", or "foundation contact"',
                                auto_focus=True,
                                width="100%",
                                size="3",
                                radius="medium",
                                variant="surface",
                                border=f"1.5px solid {BORDER_COLOR}",
                                background=rx.color_mode_cond(
                                    light="rgba(248, 249, 250, 0.95)",
                                    dark="rgba(15, 20, 28, 0.9)",
                                ),
                                color=TEXT_PRIMARY,
                                font_size="1.1rem",
                                line_height="1.5",
                                style={
                                    "& input::placeholder": {
                                        "color": rx.color_mode_cond(light="#4b5563", dark="#9ca3af"),
                                        "opacity": "1",
                                    },
                                },
                                _focus={
                                    "borderColor": ACCENT,
                                    "outline": "none",
                                },
                                _focus_within={
                                    "borderColor": ACCENT,
                                },
                            ),
                            rx.box(
                                rx.cond(
                                    State.command_palette_empty,
                                    rx.flex(
                                        rx.text("No matches found.", size="2", color=TEXT_MUTED),
                                        align="center",
                                        justify="center",
                                        height="100%",
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        rx.foreach(
                                            State.command_palette_sections,
                                            lambda entry: palette_list_entry(entry),
                                        ),
                                        spacing="2",
                                        width="100%",
                                        padding_right="0.5rem",
                                        padding_bottom="0.5rem",
                                    ),
                                ),
                                width="100%",
                                max_height="360px",
                                overflow_y="auto",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        width="min(960px, 92vw)",
                        max_width="960px",
                        background=PRIMARY_BG,
                        border_radius="14px",
                        border=f"1px solid {BORDER_COLOR}",
                        box_shadow=rx.color_mode_cond(
                            light="0 30px 120px rgba(15, 23, 42, 0.25)",
                            dark="0 30px 120px rgba(0, 0, 0, 0.8)",
                        ),
                        padding="2rem",
                        z_index="1001",
                        on_click=rx.stop_propagation,
                        opacity=rx.cond(State.command_palette_open, "1", "0"),
                        transform=rx.cond(
                            State.command_palette_open,
                            "translateY(0)",
                            "translateY(-14px)",
                        ),
                        transition="opacity 0.3s ease, transform 0.3s ease",
                        will_change="opacity, transform",
                    ),
                    position="fixed",
                    top="0",
                    left="0",
                    width="100%",
                    height="100vh",
                    z_index="1001",
                    background="rgba(6, 11, 17, 0.65)",
                    backdrop_filter="blur(12px)",
                    on_click=State.close_command_palette,
                    align_items="flex-start",
                    padding_top="8vh",
                    opacity=rx.cond(State.command_palette_open, "1", "0"),
                    transition="opacity 0.3s ease",
                    pointer_events=rx.cond(State.command_palette_open, "auto", "none"),
                ),
            ),
        ),
    )


def image_lightbox() -> rx.Component:
    """Global image lightbox driven by shared app state."""
    return rx.cond(
        State.image_lightbox_open,
        rx.center(
            rx.box(
                rx.box(
                    rx.image(
                        src=State.image_lightbox_src,
                        alt=State.image_lightbox_alt,
                        width="auto",
                        max_width="94vw",
                        max_height="86vh",
                        object_fit="contain",
                        display="block",
                    ),
                    rx.button(
                        rx.icon(tag="x", size=20),
                        id="image-lightbox-close",
                        on_click=State.close_image_lightbox,
                        variant="ghost",
                        cursor="pointer",
                        color=TEXT_PRIMARY,
                        background=rx.color_mode_cond(
                            light="rgba(255, 255, 255, 0.78)",
                            dark="rgba(13, 17, 23, 0.78)",
                        ),
                        border=f"1px solid {BORDER_COLOR}",
                        border_radius="999px",
                        width="2.25rem",
                        min_width="2.25rem",
                        height="2.25rem",
                        position="absolute",
                        top="0.75rem",
                        right="0.75rem",
                        z_index="2",
                        _hover={"color": ACCENT, "borderColor": ACCENT},
                        aria_label="Close image preview",
                    ),
                    position="relative",
                    display="inline-block",
                    border_radius="12px",
                    overflow="hidden",
                ),
                animation="lightbox-zoom-in 220ms cubic-bezier(0.22, 1, 0.36, 1)",
                will_change="transform, opacity",
                on_click=rx.stop_propagation,
            ),
            id="image-lightbox-container",
            position="fixed",
            top="0",
            left="0",
            width="100%",
            height="100vh",
            z_index="1002",
            background="rgba(6, 11, 17, 0.72)",
            backdrop_filter="blur(6px)",
            on_click=State.close_image_lightbox,
            padding="2rem",
            animation="lightbox-fade-in 180ms ease-out",
            will_change="opacity",
        ),
        rx.box(),
    )


def terminal_prompt(command: str) -> rx.Component:
    """Terminal-style command prompt."""
    return rx.flex(
        rx.text("$", color=ACCENT, weight="bold", size="3"),
        rx.text(
            command,
            color=TEXT_PRIMARY,
            size="3",
            font_family="'SF Mono', 'Monaco', monospace",
        ),
        gap="1rem",
        padding="1rem 1.5rem",
        background=CODE_BG,
        border=f"1px solid {BORDER_COLOR}",
        border_radius="8px",
        align_items="center",
        width="100%",
    )


def footer() -> rx.Component:
    """Professional footer with proper spacing."""
    nav_sections = [link for link in NAV_LINKS if link.get("children")]

    def footer_link(child: dict[str, str]) -> rx.Component:
        href = child["href"]
        return rx.link(
            child["label"],
            href=href,
            is_external=href.startswith("http"),
            color=TEXT_MUTED,
            size="3",
            _hover={"color": ACCENT},
        )

    def footer_nav_section(section: dict[str, str]) -> rx.Component:
        return rx.vstack(
            rx.text(section["label"], size="3", weight="bold", color=TEXT_PRIMARY),
            rx.vstack(
                *[footer_link(child) for child in section["children"]],
                spacing="3",
                align_items="start",
            ),
            spacing="3",
            align_items="start",
        )

    return rx.box(
        rx.box(
            rx.vstack(
                rx.grid(
                    rx.vstack(
                        rx.text("Xian Technology", size="4", weight="bold", color=TEXT_PRIMARY),
                        rx.text("Python-native contracting", size="3", color=TEXT_MUTED, line_height="1.6"),
                        spacing="2",
                        align_items="start",
                    ),
                    *[footer_nav_section(section) for section in nav_sections],
                    rx.vstack(
                        rx.text("Contact", size="3", weight="bold", color=TEXT_PRIMARY),
                        rx.hstack(
                            rx.link(
                                rx.icon(tag="mail", size=20),
                                href="mailto:info@xian.technology",
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            rx.link(
                                rx.icon(tag="message_square_text", size=20),
                                href="/contact",
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.text("Follow", size="3", weight="bold", color=TEXT_PRIMARY),
                        rx.hstack(
                            rx.link(
                                rx.icon(tag="github", size=20),
                                href="https://github.com/xian-technology",
                                is_external=True,
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            rx.link(
                                rx.icon(tag="send", size=20),
                                href="https://t.me/xian_technology",
                                is_external=True,
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            rx.link(
                                rx.icon(tag="twitter", size=20),
                                href="https://x.com/xian_technology",
                                is_external=True,
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            rx.link(
                                rx.icon(tag="youtube", size=20),
                                href="https://www.youtube.com/xian-technology",
                                is_external=True,
                                color=TEXT_PRIMARY,
                                _hover={"color": ACCENT},
                            ),
                            spacing="3",
                            align_items="center",
                        ),
                        spacing="3",
                        align_items="start",
                    ),
                    columns={
                        "initial": "1fr",
                        "sm": "repeat(2, minmax(0, 1fr))",
                        "md": "repeat(3, minmax(0, 1fr))",
                        "lg": "repeat(5, minmax(0, 1fr))",
                    },
                    gap=rx.breakpoints(initial="1.75rem", md="2.25rem", lg="3rem"),
                    width="100%",
                    align_items="start",
                ),
                rx.box(
                    rx.flex(
                        rx.text("© 2025 Xian Technology. Built with 💚 and 🐍", size="2", color=TEXT_MUTED),
                        gap="0.35rem",
                        align_items="center",
                        justify="center",
                        wrap="wrap",
                        width="100%",
                    ),
                    padding_top="3rem",
                    border_top=f"1px solid {BORDER_COLOR}",
                    width="100%",
                ),
                spacing="6",
                width="100%",
            ),
            max_width=MAX_CONTENT_WIDTH,
            margin="0 auto",
            padding="4rem 2rem",
        ),
        background=rx.color_mode_cond(
            light="linear-gradient(180deg, rgba(238, 243, 248, 0) 0%, #eef3f8 2%, #eef3f8 100%)",
            dark="linear-gradient(180deg, rgba(16, 26, 38, 0) 0%, #101a26 2%, #101a26 100%)",
        ),
        width="100%",
        transition="background-color 0.3s ease",
    )


def page_layout(*children: rx.Component) -> rx.Component:
    """Base layout wrapper for all pages."""
    gradient_overlay = rx.box(
        background=TOP_GRADIENT,
        position="absolute",
        top="0",
        left="0",
        right="0",
        height="520px",
        pointer_events="none",
        z_index="0",
    )
    return rx.box(
        gradient_overlay,
        command_palette(),
        image_lightbox(),
        rx.box(
            nav_bar(),
            rx.box(
                *children,
                min_height="calc(100vh - 200px)",
                padding_bottom="2rem",
            ),
            footer(),
            position="relative",
            z_index="1",
        ),
        position="relative",
        background=PRIMARY_BG,
        color=TEXT_PRIMARY,
        min_height="100vh",
        transition="background-color 0.3s ease, color 0.3s ease",
    )


__all__ = [
    "copyable_code_block",
    "command_palette",
    "command_palette_button",
    "code_block",
    "feature_card",
    "hover_icon_chip",
    "image_lightbox",
    "inline_code",
    "icon_watermark_hover_card",
    "nav_bar",
    "nav_link",
    "page_layout",
    "section",
    "section_action_links",
    "section_panel",
    "subsection",
    "terminal_prompt",
    "text_with_inline_code",
    "theme_toggle",
]
