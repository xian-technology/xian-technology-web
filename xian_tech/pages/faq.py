from typing import Any

import reflex as rx

from ..components.common import page_layout, section
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    BORDER_COLOR,
    SURFACE,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

SEARCH_SECTIONS = [
    {
        "title": "Frequently Asked Questions",
        "subtitle": "Answers about the foundation, stack, and how to get involved.",
        "category": "About",
        "badge": "Page",
        "href": "/faq",
        "keywords": ["FAQ", "Questions", "Foundation", "Stack"],
    }
]

FAQ_ITEMS = [
    {
        "id": "xian-network",
        "question": "What is the Xian Network and what is its goal?",
        "answer": [
            (
                "The Xian Network is an independent Layer 1 blockchain that runs on the Xian Technology stack. "
                "Its goal is to prove that the stack works in a real-world environment while staying simple to use."
            ),
            (
                "It is not a demo network. It is a live cryptocurrency project with a bridge to Solana and exchange "
                "listings, integrated into the broader crypto ecosystem. The long-term goal is full decentralization "
                "and a strong platform for Python developers to build smart contracts and applications. Learn more at xian.org."
            ),
        ],
    },
    {
        "id": "top-100",
        "question": "Can the Xian Network become a top 100 cryptocurrency?",
        "answer": [
            (
                "In theory, yes. The network is fast, offers Ethereum-class contract capabilities, and lowers the barrier "
                "to entry by using Python."
            ),
            (
                "Realistically, a top-100 position is unlikely without significant funding and marketing. The original project "
                "that created the contracting engine raised around $12M but later dissolved, leaving the community without "
                "resources. The current Xian Network effort was started with roughly $150k from dedicated supporters—an amount "
                "that is meaningful for core development but not enough for large-scale promotion in a crowded market."
            ),
        ],
    },
    {
        "id": "xian-performance",
        "question": "How fast can a Xian Technology based blockchain be, and what's the TPS?",
        "answer": [
            (
                "Because every transaction is a Python contract call, performance is constrained by Python's execution speed. "
                "Even so, early stress tests during Xian Network development observed roughly 2,200 transactions per 2-second block "
                "(about 1,100 TPS)."
            ),
            (
                "The current ABCI app runs transactions sequentially and has not yet been optimized for throughput. Parallelism and "
                "further tuning are planned, but the existing performance is already sufficient for current needs."
            ),
        ],
    },
    {
        "id": "lamden-connection",
        "question": "What's the connection between Lamden and Xian?",
        "answer": [
            (
                "Lamden was a cryptocurrency project created in 2017 by Stuart Farmer and the original source of the "
                "Python contracting engine."
            ),
            (
                "Lamden was discontinued in 2023 due largely to financial constraints. Xian was created by Lamden community "
                "developers (Duelingbenjos, Endogen, and Crosschainer) to continue advancing the contracting engine, but "
                "they replaced Lamden's custom node with CometBFT, which now anchors the Xian Technology stack."
            ),
        ],
    },
    {
        "id": "xian-name",
        "question": "Where does the name Xian come from?",
        "answer": [
            (
                "Xian refers to mythological immortals in Chinese tradition, associated with transcendence, resilience, "
                "and renewal."
            ),
            (
                "The name reflects the project's history: it lived on after Lamden ended and was effectively reborn as a "
                "new community-led network and technology stack. Xian is meant to signal a project that does not die, but "
                "evolves."
            ),
        ],
    },
    {
        "id": "foundation-connection",
        "question": "What exactly is the Xian Foundation and what is its connection to the Xian Network?",
        "answer": [
            (
                "The Xian Foundation is a small group of software engineers focused on advancing the Xian Technology stack "
                "into a complete, easy-to-integrate platform."
            ),
            (
                "It is a working group rather than a registered legal entity, and it does not hold or require assets to "
                "execute its mission. The foundation is led by David Strohmayer, who is also a founder and core developer "
                "of the Xian Network, while the network itself remains independent."
            ),
        ],
    },
    {
        "id": "foundation-origin",
        "question": "How and why was the Xian Foundation created?",
        "answer": [
            (
                "The foundation was created by David Strohmayer, a core developer of the Xian Network, to focus on the technology "
                "itself. The Xian Network's day-to-day needs prioritized adoption and ecosystem growth, leaving less room to refine "
                "the core stack."
            ),
            (
                "The foundation exists to close that gap by driving the software platform forward and improving the out-of-the-box "
                "developer experience."
            ),
            (
                "It does not operate a standalone website. Instead, it is integrated into the Xian Technology site, which was built "
                "as a first step to create a single entry point for everything related to Xian and the technology stack."
            ),
        ],
    },
    {
        "id": "foundation-fulltime",
        "question": "Is anyone at the Xian Foundation or Xian Network working full time on Xian?",
        "answer": [
            (
                "No. The core contributors work on Xian in their free time so the project never depends on funding to keep "
                "moving forward. Continuing to build the Xian technology stack without direct financial incentives also "
                "signals long-term commitment and belief in the mission."
            ),
        ],
    },
    {
        "id": "foundation-vision",
        "question": "What's the vision of the Xian Foundation?",
        "answer": [
            (
                "Build Xian Technology into a robust stack that individuals, communities, and companies can set up quickly."
            ),
            (
                "The aim is to make launching decentralized or distributed networks simple, with sensible defaults and enough "
                "flexibility to customize when needed."
            ),
        ],
    },
    {
        "id": "use-xian-tech",
        "question": "Can I use Xian Technology for my own crypto project?",
        "answer": [
            (
                "Yes. The software is open source, and the contracting engine is licensed under GPLv3. As long as you comply "
                "with the license, you can use it and other parts of the stack in your own projects."
            )
        ],
    },
    {
        "id": "get-involved",
        "question": "I'm a Python developer and I'd like to get involved. How?",
        "answer": [
            (
                "Great to hear. The best way to start is by opening a pull request on one of the Xian repositories or by reaching "
                "out via our social channels."
            ),
            rx.text(
                "You can browse the Xian Foundation repositories at ",
                rx.link(
                    "https://github.com/orgs/xian-technology/repositories",
                    href="https://github.com/orgs/xian-technology/repositories",
                    is_external=True,
                    color=ACCENT,
                    _hover={"color": ACCENT},
                ),
                ". Contributors who make meaningful contributions to the ecosystem can be invited to the foundation.",
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
            ),
        ],
    },
]


def _faq_item(item: dict[str, Any]) -> rx.Component:
    """Single FAQ entry with expandable detail."""
    overlay_background = rx.color_mode_cond(
        light=(
            "linear-gradient(135deg, rgba(80, 177, 101, 0.2), rgba(80, 177, 101, 0.08)), "
            "linear-gradient(to right, rgba(128, 128, 128, 0.08) 1px, transparent 1px), "
            "linear-gradient(to bottom, rgba(128, 128, 128, 0.08) 1px, transparent 1px)"
        ),
        dark=(
            "linear-gradient(135deg, rgba(0, 255, 136, 0.14), rgba(0, 255, 136, 0.05)), "
            "linear-gradient(to right, rgba(255, 255, 255, 0.06) 1px, transparent 1px), "
            "linear-gradient(to bottom, rgba(255, 255, 255, 0.06) 1px, transparent 1px)"
        ),
    )
    watermark_color = rx.color_mode_cond(
        light="rgba(46, 140, 71, 0.15)",
        dark="rgba(0, 255, 136, 0.08)",
    )

    answer_blocks = [
        rx.text(
            paragraph,
            size="3",
            color=TEXT_MUTED,
            line_height="1.7",
        )
        if isinstance(paragraph, str)
        else paragraph
        for paragraph in item["answer"]
    ]

    return rx.accordion.item(
        rx.accordion.header(
            rx.accordion.trigger(
                rx.hstack(
                    rx.text(
                        item["question"],
                        size="4",
                        weight="bold",
                        color=TEXT_PRIMARY,
                        text_align="left",
                        flex="1",
                        min_width="0",
                    ),
                    rx.accordion.icon(color=TEXT_MUTED, flex_shrink="0"),
                    justify="between",
                    align_items="start",
                    width="100%",
                ),
                padding="1.5rem",
                background="transparent",
                box_shadow="none",
                color=TEXT_PRIMARY,
                text_align="left",
                cursor="pointer",
                width="100%",
                _hover={"backgroundColor": "transparent"},
            )
        ),
        rx.accordion.content(
            rx.box(
                rx.vstack(
                    *answer_blocks,
                    spacing="3",
                    align_items="start",
                ),
                padding_left="1.5rem",
                padding_right="1.5rem",
                padding_bottom="1.5rem",
            ),
            color=TEXT_MUTED,
        ),
        value=f"faq-{item['id']}",
        background=SURFACE,
        border_radius="14px",
        border=f"1px solid {BORDER_COLOR}",
        transition="all 0.2s ease",
        overflow="hidden",
        position="relative",
        _hover={
            "borderColor": ACCENT,
            "boxShadow": rx.color_mode_cond(
                light="0 12px 28px rgba(80, 177, 101, 0.16)",
                dark="0 12px 28px rgba(0, 255, 136, 0.18)",
            ),
        },
        style={
            "& > *": {
                "position": "relative",
                "zIndex": "1",
            },
            "&::before": {
                "content": '""',
                "position": "absolute",
                "inset": "0",
                "backgroundImage": overlay_background,
                "backgroundSize": "auto, 20px 20px, 20px 20px",
                "opacity": "0",
                "transition": "opacity 0.55s ease",
                "pointerEvents": "none",
                "zIndex": "0",
            },
            "&::after": {
                "content": '"?"',
                "position": "absolute",
                "right": "-0.35rem",
                "bottom": "-0.75rem",
                "fontSize": "7.5rem",
                "lineHeight": "1",
                "fontWeight": "700",
                "color": watermark_color,
                "opacity": "0",
                "transform": "rotate(12deg) scale(1.85)",
                "transition": "opacity 0.7s ease, transform 0.7s ease",
                "pointerEvents": "none",
                "zIndex": "0",
            },
            "&:hover::before": {
                "opacity": "1",
            },
            "&:hover::after": {
                "opacity": "1",
                "transform": "rotate(0deg) scale(1.85)",
            },
            "&:first-child": {
                "border_top_left_radius": "14px",
                "border_top_right_radius": "14px",
            },
            "&:last-child": {
                "border_bottom_left_radius": "14px",
                "border_bottom_right_radius": "14px",
            },
        },
        width="100%",
    )


def faq_page() -> rx.Component:
    """FAQ page."""
    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("FAQ", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Frequently Asked Questions",
                    size="8",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    line_height="1.2",
                ),
                rx.text(
                    "Answers to common questions about the foundation, the Xian stack, and how to get involved.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    max_width="900px",
                ),
                rx.accordion.root(
                    *[_faq_item(item) for item in FAQ_ITEMS],
                    type="single",
                    collapsible=True,
                    variant="outline",
                    width="100%",
                    show_dividers=False,
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "gap": "1rem",
                        "border": "none",
                        "boxShadow": "none",
                        "backgroundColor": "transparent",
                        "&[data-variant='outline']": {
                            "border": "none",
                            "boxShadow": "none",
                            "backgroundColor": "transparent",
                        },
                    },
                ),
                spacing="6",
                align_items="start",
                width="100%",
            )
        )
    )


__all__ = ["faq_page"]
