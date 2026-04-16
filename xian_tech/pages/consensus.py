import reflex as rx

from ..components.common import (
    hover_icon_chip,
    icon_watermark_hover_card,
    linked_heading,
    page_layout,
    section,
    section_action_links,
    section_panel,
    subsection,
)
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

SEARCH_SECTIONS = [
    {
        "title": "CometBFT Consensus",
        "subtitle": "Byzantine fault-tolerant replication with a language-agnostic ABCI interface.",
        "category": "Technology",
        "badge": "Page",
        "href": "/consensus",
        "keywords": ["CometBFT", "Consensus", "ABCI", "BFT"],
    },
    {
        "title": "Language-agnostic application layer",
        "subtitle": "ABCI lets the application be written in any language while CometBFT handles consensus.",
        "category": "Technology",
        "badge": "Section",
        "href": "/consensus",
        "keywords": ["ABCI", "Application", "Language-agnostic"],
    },
    {
        "title": "ABCI execution flow",
        "subtitle": "CheckTx, FinalizeBlock, and Commit coordinate validation and state changes.",
        "category": "Technology",
        "badge": "Section",
        "href": "/consensus",
        "keywords": ["CheckTx", "FinalizeBlock", "Commit"],
    },
    {
        "title": "Security and extensibility",
        "subtitle": "ABCI++ hooks and evidence handling for advanced consensus workflows.",
        "category": "Technology",
        "badge": "Section",
        "href": "/consensus",
        "keywords": ["ABCI++", "Evidence", "Validators"],
    },
    {
        "title": "How it works",
        "subtitle": "Propose, prevote, precommit, commit—the simplified consensus flow.",
        "category": "Technology",
        "badge": "Section",
        "href": "/consensus",
        "keywords": ["Propose", "Prevote", "Precommit", "Commit"],
    },
]


def consensus_page() -> rx.Component:
    """CometBFT consensus overview."""
    def info_card(title: str, body: str, icon: str = "circle_help") -> rx.Component:
        return icon_watermark_hover_card(
            rx.heading(title, size="5", color=TEXT_PRIMARY, weight="bold"),
            rx.text(body, size="3", color=TEXT_MUTED, line_height="1.7"),
            icon=icon,
            padding="2.25rem",
        )

    def choice_card(title: str, body: str, icon: str) -> rx.Component:
        return icon_watermark_hover_card(
            rx.flex(
                hover_icon_chip(icon),
                rx.heading(title, size="5", weight="bold", color=TEXT_PRIMARY),
                direction={"base": "row", "lg": "column"},
                align={"base": "center", "lg": "start"},
                spacing="3",
            ),
            rx.text(body, size="3", color=TEXT_MUTED, line_height="1.7"),
            icon=icon,
            padding="2rem",
        )

    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("CONSENSUS", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Network Consensus",
                    size="8",
                    color=TEXT_PRIMARY,
                    line_height="1.15",
                    weight="bold",
                ),
                rx.text(
                    "Network consensus keeps all validators aligned on one ordered history so blocks are finalized "
                    "predictably and every node sees the same state. CometBFT provides this foundation for Xian, giving "
                    "us a reliable, fast consensus core to build Python-first applications on top of.",
                    size="4",
                    color=TEXT_MUTED,
                    width="100%",
                    line_height="1.7",
                ),
                spacing="6",
                align_items="start",
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("CometBFT", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [
                                {"label": "Repo", "icon": "github", "href": "https://github.com/cometbft/cometbft"},
                                {"label": "DeepWiki", "icon": "brain", "href": "https://deepwiki.com/cometbft/cometbft"},
                                {"label": "Docs", "icon": "book_open", "href": "https://docs.cometbft.com/v0.39"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "CometBFT provides Byzantine fault-tolerant state machine replication and delivers the same ordered "
                        "transaction log to every non-faulty node. It separates consensus from the application state via ABCI, "
                        "so Xian can use its Python contracting engine while relying on a proven consensus core. "
                        "CometBFT itself is implemented in Go for performance, while Xian keeps the user-facing stack in Python.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.grid(
                    choice_card(
                        "Security",
                        "Byzantine fault tolerance keeps the network secure as long as less than one-third of voting power is byzantine.",
                        "shield",
                    ),
                    choice_card(
                        "Scalability",
                        "CometBFT is designed for high throughput and is reported to reach thousands of TPS; real results depend on the application and configuration.",
                        "layers",
                    ),
                    choice_card(
                        "Interoperability",
                        "ABCI enables application-specific chains, and the Cosmos ecosystem uses CometBFT to connect independent networks.",
                        "link",
                    ),
                    choice_card(
                        "Fast finality",
                        "Blocks finalize in seconds once more than two-thirds precommit, delivering deterministic settlement without reorgs.",
                        "bolt",
                    ),
                    choice_card(
                        "Developer freedom",
                        "ABCI lets developers write chain logic in their language of choice while CometBFT handles consensus and networking.",
                        "code",
                    ),
                    choice_card(
                        "Modernized Tendermint",
                        "CometBFT is the fork and successor to Tendermint Core, continuing the design with efficiency improvements for today’s networks.",
                        "satellite",
                    ),
                    columns={
                        "base": "repeat(1, minmax(0, 1fr))",
                        "md": "repeat(2, minmax(0, 1fr))",
                        "lg": "repeat(3, minmax(0, 1fr))",
                    },
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Properties",
                    rx.text(
                        "Additionally, the following properties make CometBFT the perfect choice for us. "
                        "They reinforce reliability, help the network stay consistent under load, and keep the "
                        "consensus layer predictable so the Python application layer can stay focused on contracts.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.grid(
                        choice_card(
                            "BFT replication",
                            "CometBFT keeps every non-faulty node on the same ordered transaction log and tolerates Byzantine failures below one-third of the validator set.",
                            "shield",
                        ),
                        choice_card(
                            "Consensus engine + ABCI",
                            "The consensus engine is decoupled from the application via ABCI, so the state machine can be written in any language.",
                            "link",
                        ),
                        choice_card(
                            "Mempool validation",
                            "CheckTx validates incoming transactions and only relays valid ones to peers before they enter consensus.",
                            "check",
                        ),
                        choice_card(
                            "Multi-connection ABCI",
                            "CometBFT maintains multiple ABCI connections (mempool, consensus, snapshot, and query) to keep responsibilities separated.",
                            "layers",
                        ),
                        choice_card(
                            "Instant finality",
                            "Blocks finalize deterministically—no probabilistic forks or reorgs once a block is committed.",
                            "bolt",
                        ),
                        choice_card(
                            "Light client protocol",
                            "CometBFT specifies a light client protocol for securely verifying the latest state without running a full node.",
                            "satellite",
                        ),
                        columns={
                            "base": "repeat(1, minmax(0, 1fr))",
                            "md": "repeat(2, minmax(0, 1fr))",
                            "lg": "repeat(3, minmax(0, 1fr))",
                        },
                        spacing="4",
                        width="100%",
                        align="stretch",
                    ),
                ),
                subsection(
                    "How it works",
                    rx.text(
                        "Validators take turns proposing blocks and voting, weighted by their stake. Each round moves "
                        "through propose, prevote (for a block or nil), and precommit (for a block or nil). A block is "
                        "committed once more than two-thirds of voting power precommits the same block; otherwise the "
                        "process advances to a new round until consensus is reached, delivering deterministic finality.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.image(
                        src="/cometbft.png",
                        alt="CometBFT consensus flow diagram",
                        width="100%",
                        max_width="960px",
                        border_radius="12px",
                        align_self="center",
                    ),
                ),
            ),
        ),
    )


__all__ = ["consensus_page"]
