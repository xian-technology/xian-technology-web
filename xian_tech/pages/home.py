import reflex as rx

from ..components.common import (
    hover_icon_chip,
    icon_watermark_hover_card,
    linked_heading,
    page_layout,
    section,
)
from ..data import CORE_COMPONENTS, NOTEWORTHY_QUOTES
from ..state import State
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_HOVER,
    ACCENT_SOFT,
    BORDER_COLOR,
    PRIMARY_BG,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

QUOTE_GAP = "1.5rem"
QUOTE_GAP_HALF = "0.75rem"


SEARCH_SECTIONS = [
    {
        "title": "Python-First Decentralized Infrastructure",
        "subtitle": "Programmable networks, easy smart contracts, and software-friendly integration.",
        "category": "Home",
        "badge": "Hero",
        "href": "/",
        "keywords": ["Python", "Programmable networks", "Integration", "Smart contracts"],
    },
    {
        "title": "Why Xian?",
        "subtitle": "Decentralized infrastructure that can be used like a tool, not just a chain.",
        "category": "Home",
        "badge": "Section",
        "href": "/",
        "keywords": ["Infrastructure", "Tool", "Programmable networks", "Adoption"],
    },
    {
        "title": "Why Python?",
        "subtitle": "Python-first contracts that optimize for clarity, integration, and ease of use.",
        "category": "Home",
        "badge": "Section",
        "href": "/",
        "keywords": ["Python", "Contracts", "Integration", "Usability"],
    },
    {
        "title": "Quotes on Python",
        "subtitle": "Rotating highlights from teams and leaders using Python.",
        "category": "Home",
        "badge": "Section",
        "href": "/",
        "keywords": ["Quotes", "Python", "Community"],
    },
]


def hero_section() -> rx.Component:
    """Hero section for the landing page."""
    return section(
        rx.vstack(
            rx.box(
                rx.text(
                    "XIAN_TECHNOLOGY",
                    size="2",
                    letter_spacing="0.15em",
                    color=ACCENT,
                    weight="medium",
                ),
                padding="0.625rem 1.25rem",
                background=ACCENT_SOFT,
                border=f"1px solid {ACCENT_GLOW}",
                border_radius="8px",
            ),
            rx.heading(
                "Python-First Infrastructure for Programmable Networks",
                size="9",
                line_height="1.1",
                color=TEXT_PRIMARY,
                max_width="900px",
                text_align="center",
                weight="bold",
            ),
            rx.text(
                "Xian is a Python-first decentralized application platform. Build app-specific "
                "networks, write simple but powerful smart contracts, and integrate programmable "
                "shared state into normal software systems without adopting a highly specialized stack.",
                size="5",
                color=TEXT_MUTED,
                max_width="700px",
                text_align="center",
                line_height="1.7",
            ),
            rx.flex(
                rx.link(
                    rx.button(
                        rx.flex(
                            rx.text("View on GitHub", size="3", weight="medium"),
                            rx.text(
                                "→",
                                weight="bold",
                                size="4",
                                class_name="github-arrow",
                                style={"transition": "transform 0.2s ease"},
                            ),
                            gap="0.75rem",
                            align_items="center",
                        ),
                        size="4",
                        background_color=ACCENT,
                        color=PRIMARY_BG,
                        border_radius="10px",
                        padding="1.25rem 2rem",
                        cursor="pointer",
                        _hover={
                            "backgroundColor": ACCENT_HOVER,
                            "boxShadow": f"0 12px 30px {ACCENT_SOFT}",
                            "& .github-arrow": {"transform": "translateX(6px)"},
                        },
                        transition="all 0.2s ease",
                    ),
                    href="https://github.com/xian-technology",
                    is_external=True,
                ),
                gap="1.5rem",
                wrap="wrap",
                justify="center",
            ),
            spacing="8",
            align_items="center",
            width="100%",
        ),
        padding_top="2.67rem",
        padding_bottom="3rem",
    )


def stack_overview() -> rx.Component:
    """Stack overview grid."""
    def overview_card(item: dict[str, str]) -> rx.Component:
        return rx.link(
            icon_watermark_hover_card(
                rx.flex(
                    hover_icon_chip(item["icon"]),
                    rx.heading(item["title"], size="5", weight="bold", color=TEXT_PRIMARY),
                    direction={"base": "row", "lg": "column"},
                    align={"base": "center", "lg": "start"},
                    spacing="3",
                ),
                rx.text(item["description"], size="3", color=TEXT_MUTED, line_height="1.7"),
                icon=item["icon"],
            ),
            href=item["href"],
            _hover={"textDecoration": "none"},
        )

    return section(
        rx.vstack(
            rx.text(
                "A streamlined stack for running programmable decentralized networks with clear execution, strong tooling, and software-friendly integration surfaces.",
                size="4",
                color=TEXT_MUTED,
                max_width="820px",
                line_height="1.7",
                text_align="center",
            ),
            rx.grid(
                *[overview_card(item) for item in CORE_COMPONENTS],
                columns={
                    "base": "repeat(1, minmax(0, 1fr))",
                    "md": "repeat(2, minmax(0, 1fr))",
                    "lg": "repeat(4, minmax(0, 1fr))",
                },
                spacing="4",
                width="100%",
                align="stretch",
            ),
            spacing="6",
            align_items="center",
        ),
        padding_top="3rem",
        padding_bottom="3rem",
    )


def mission_section() -> rx.Component:
    """Mission overview for the foundation."""
    def bullet(text: str) -> rx.Component:
        return rx.flex(
            rx.text("→", color=ACCENT, size="3"),
            rx.text(text, size="3", color=TEXT_MUTED, line_height="1.6"),
            gap="0.65rem",
            align_items="center",
        )

    return section(
        rx.vstack(
            linked_heading("Our Mission", size="7", color=TEXT_PRIMARY, weight="bold"),
            rx.text(
                "The Xian Technology Foundation advances Xian as a Python-first decentralized application platform that stays simple, flexible, and operationally clear.",
                size="4",
                color=TEXT_MUTED,
                line_height="1.7",
            ),
            rx.grid(
                icon_watermark_hover_card(
                    rx.heading("Keep it simple & powerful", size="5", color=TEXT_PRIMARY, weight="bold"),
                    bullet("Keep ABCI and the contracting engine clean, deterministic, and auditable."),
                    bullet("Maintain compatibility with new Python interpreters without breaking contracts."),
                    icon="shield",
                    padding="2.5rem",
                ),
                icon_watermark_hover_card(
                    rx.heading("Extend functionality", size="5", color=TEXT_PRIMARY, weight="bold"),
                    bullet("Evolve node features and operational insight."),
                    bullet("Ship and maintain high-value system contracts."),
                    bullet("Deliver tools (CLI, SDKs, services) to interface easily with Xian."),
                    icon="puzzle",
                    padding="2.5rem",
                ),
                icon_watermark_hover_card(
                    rx.heading("Make networks easy to run", size="5", color=TEXT_PRIMARY, weight="bold"),
                    bullet("Smooth setup for local nodes and multi-node environments."),
                    bullet("Documented patterns for distributed production networks."),
                    icon="network",
                    padding="2.5rem",
                ),
                icon_watermark_hover_card(
                    rx.heading("Document everything", size="5", color=TEXT_PRIMARY, weight="bold"),
                    bullet("Explain how the stack works and how to build on it and interface with it."),
                    bullet("Keep upgrade paths, examples, and reference guides current."),
                    icon="book_open",
                    padding="2.5rem",
                ),
                columns={
                    "base": "repeat(1, minmax(0, 1fr))",
                    "md": "repeat(2, minmax(0, 1fr))",
                },
                rows="2",
                flow="row",
                gap="1.5rem",
                width="100%",
                align="stretch",
            ),
            spacing="6",
            align_items="start",
        ),
        padding_top="3rem",
        padding_bottom="3rem",
    )


def why_another_blockchain() -> rx.Component:
    """Explain why Xian exists."""
    return section(
        rx.grid(
            rx.vstack(
                linked_heading("Why Xian?", size="7", color=TEXT_PRIMARY, weight="bold"),
                rx.text(
                    "Xian exists for teams that need decentralized coordination or shared programmable state, but do not want to adopt a niche contract language or a hard-to-operate blockchain stack. The aim is to make decentralized infrastructure feel more like a practical software tool and less like a specialized ecosystem you have to re-learn from scratch.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                ),
                spacing="4",
                align_items="start",
            ),
            template_columns={"base": "1fr", "md": "repeat(1, 1fr)"},
            gap="1.5rem",
            width="100%",
        ),
        rx.box(
            rx.text(
                rx.fragment(
                    "A practical example of the broader shift is ",
                    rx.link(
                        "Google’s Universal Ledger (GCUL)",
                        href="https://cloud.google.com/application/web3/universal-ledger",
                        is_external=True,
                        color=ACCENT,
                    ),
                    ": a managed, programmable ledger on familiar cloud primitives. It reflects the same general direction: programmable ledger infrastructure becoming easier to embed into normal software and operations environments.",
                ),
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
            ),
            margin_top="1rem",
        ),
        rx.box(
            rx.text(
                "The Xian software stack aims to be a free, open alternative in that direction: ready to run on-prem or in the cloud, easy to adapt, and suited for application-specific decentralized projects that value clarity, flexibility, and integration.",
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
            ),
            margin_top="0.5rem",
        ),
        padding_top="3rem",
        padding_bottom="3rem",
    )


def why_python() -> rx.Component:
    """Explain the Python-first choice."""
    def trend_image(src: str, alt: str, source: str, description: str) -> rx.Component:
        overlay_bg = rx.color_mode_cond(
            light="linear-gradient(180deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.82) 45%, rgba(255, 255, 255, 0.95) 100%)",
            dark="linear-gradient(180deg, rgba(10, 14, 20, 0) 0%, rgba(10, 14, 20, 0.78) 45%, rgba(10, 14, 20, 0.95) 100%)",
        )
        return rx.box(
            rx.image(
                src=src,
                alt=alt,
                width="100%",
                height=rx.breakpoints(initial="200px", md="220px", lg="240px"),
                object_fit="cover",
            ),
            rx.box(
                rx.text(
                    description,
                    size="2",
                    color=TEXT_PRIMARY,
                    line_height="1.6",
                ),
                class_name="trend-overlay",
                position="absolute",
                bottom="0",
                left="0",
                right="0",
                height="75%",
                padding="1rem",
                background=overlay_bg,
                transform="translateY(100%)",
                opacity="0",
                transition="transform 0.35s ease, opacity 0.35s ease",
                pointer_events="none",
                z_index="1",
                align_items="end",
                display="flex",
            ),
            rx.link(
                rx.badge(
                    "Source",
                    variant="soft",
                    color_scheme="green",
                    radius="medium",
                    size="2",
                ),
                href=source,
                is_external=True,
                position="absolute",
                bottom="0.33rem",
                right="0.33rem",
                on_click=rx.stop_propagation,
                z_index="2",
                _hover={"textDecoration": "none"},
            ),
            position="relative",
            width="100%",
            cursor="zoom-in",
            border_radius="12px",
            border=f"2px solid {BORDER_COLOR}",
            box_shadow=f"0 0 18px {ACCENT_SOFT}",
            overflow="hidden",
            style={
                "&:hover .trend-overlay": {
                    "transform": "translateY(0)",
                    "opacity": "1",
                }
            },
            on_click=State.open_image_lightbox(src, alt),
        )

    return section(
        rx.grid(
            rx.vstack(
                linked_heading(
                    "Why Python?",
                    size="7",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    anchor_id="why-python-trends",
                ),
                rx.text(
                    "Python is one of the most used programming languages worldwide but is still underused in decentralized infrastructure. At Xian, the developer-facing story is Python-first because the goal is to make programmable networks easier to understand, integrate, and operate. The point is not to win raw throughput benchmarks; it is to make the useful parts of decentralization easier for normal engineering teams to adopt.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                ),
                rx.text(
                    "Take a look at current programming language trends and see how Python dominates.",
                    size="3",
                    color=TEXT_MUTED,
                    line_height="1.7",
                ),
                spacing="4",
                align_items="start",
            ),
            rx.box(
                rx.grid(
                    trend_image(
                        "/github.png",
                        "Programming languages on GitHub",
                        "https://github.blog/news-insights/octoverse/octoverse-2024",
                        "Top programming languages on GitHub, ranked by the number of distinct contributors per language.",
                    ),
                    trend_image(
                        "/languish.png",
                        "Programming language trends from Languish",
                        "https://tjpalmer.github.io/languish",
                        "Language trends based on the mean of GitHub stars and Stack Overflow question counts.",
                    ),
                    trend_image(
                        "/tiobe.png",
                        "TIOBE index ranking snapshot",
                        "https://www.tiobe.com/tiobe-index",
                        "The TIOBE index tracks language popularity using signals like global engineer counts, courses, and vendors.",
                    ),
                    columns={"base": "1fr", "md": "repeat(3, minmax(0, 1fr))"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                display="flex",
                justify_content="center",
            ),
            template_columns={"base": "1fr", "md": "repeat(2, 1fr)"},
            gap="2rem",
        ),
        padding_top="3rem",
        padding_bottom="3rem",
    )


def noteworthy_quotes() -> rx.Component:
    """Showcase notable quotes about Python and technology."""
    quotes = NOTEWORTHY_QUOTES
    items = quotes if len(quotes) == 1 else quotes * 4
    card_width = rx.breakpoints(initial="260px", sm="300px", md="340px")
    animation_style = "quote-marquee 55s linear infinite" if len(quotes) > 1 else "none"
    fade_left = rx.color_mode_cond(
        light="linear-gradient(90deg, #ffffff 0%, rgba(255, 255, 255, 0) 100%)",
        dark="linear-gradient(90deg, #0a0e14 0%, rgba(10, 14, 20, 0) 100%)",
    )
    fade_right = rx.color_mode_cond(
        light="linear-gradient(270deg, #ffffff 0%, rgba(255, 255, 255, 0) 100%)",
        dark="linear-gradient(270deg, #0a0e14 0%, rgba(10, 14, 20, 0) 100%)",
    )

    def quote_card(item: dict[str, str]) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.text("“", size="7", color=ACCENT, weight="bold", line_height="0.6"),
                rx.text(item["quote"], size="2", color=TEXT_MUTED, line_height="1.6", font_style="italic"),
                rx.hstack(
                    rx.spacer(),
                    rx.text("”", size="7", color=ACCENT, weight="bold", line_height="0.6"),
                    width="100%",
                ),
                rx.hstack(
                    rx.box(width="5px", height="5px", border_radius="50%", background=ACCENT),
                    rx.text(item["author"], size="1", color=TEXT_MUTED, weight="medium"),
                    rx.link(
                        "Source",
                        href=item["source"],
                        is_external=True,
                        color=ACCENT,
                        size="1",
                        _hover={"textDecoration": "none"},
                    ),
                    gap="0.6rem",
                    align_items="center",
                    wrap="wrap",
                ),
                spacing="1",
                align_items="start",
                width="100%",
            ),
            padding="1rem",
            background=rx.color_mode_cond(
                light="rgba(0, 179, 92, 0.14)",
                dark=ACCENT_SOFT,
            ),
            border_radius="12px",
            box_shadow=f"0 0 18px {ACCENT_SOFT}",
            width=card_width,
            min_width=card_width,
            flex="0 0 auto",
        )

    return section(
        rx.vstack(
            linked_heading("Quotes on Python", size="6", color=TEXT_PRIMARY, weight="bold"),
            rx.box(
                rx.flex(
                    *[quote_card(item) for item in items],
                    class_name="quote-track",
                    direction="row",
                    gap=QUOTE_GAP,
                    align_items="stretch",
                    style={
                        "width": "max-content",
                        "animation": animation_style,
                        "animationPlayState": "running",
                        "--quote-gap": QUOTE_GAP,
                        "--quote-gap-half": QUOTE_GAP_HALF,
                    },
                    _hover={
                        "animationPlayState": "paused",
                    },
                ),
                rx.box(
                    position="absolute",
                    top="0",
                    bottom="0",
                    left="0",
                    width="2rem",
                    background=fade_left,
                    pointer_events="none",
                    z_index="1",
                ),
                rx.box(
                    position="absolute",
                    top="0",
                    bottom="0",
                    right="0",
                    width="2rem",
                    background=fade_right,
                    pointer_events="none",
                    z_index="1",
                ),
                width="100%",
                overflow="hidden",
                position="relative",
            ),
            spacing="4",
            align_items="start",
        ),
        padding_top="0rem",
        padding_bottom="3rem",
    )


def home_page() -> rx.Component:
    """Landing page entry point."""
    return page_layout(
        hero_section(),
        stack_overview(),
        mission_section(),
        why_another_blockchain(),
        why_python(),
        noteworthy_quotes(),
    )


__all__ = ["home_page"]
