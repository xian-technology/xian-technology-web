import reflex as rx

from ..components.common import (
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
        "title": "API References",
        "subtitle": "Reference endpoints for CometBFT RPC, BDS, transactions, and contracts.",
        "category": "Developers",
        "badge": "Page",
        "href": "/api",
        "keywords": ["API", "References", "RPC", "CometBFT", "BDS", "Endpoints"],
    }
]

RPC_DOCS_BASE = "https://docs.cometbft.com/main/rpc/#"

RPC_SECTIONS = [
    {
        "title": "Info Routes",
        "description": (
            "Read-only endpoints for node health, block/validator data, mempool visibility, and chain state introspection. "
            "Use these for dashboards, monitoring, and explorers."
        ),
        "items": [
            {"name": "Health", "operation_id": "health", "tag": "Info", "description": "Node heartbeat."},
            {"name": "Status", "operation_id": "status", "tag": "Info", "description": "Node status."},
            {"name": "NetInfo", "operation_id": "net_info", "tag": "Info", "description": "Network information."},
            {
                "name": "Blockchain",
                "operation_id": "blockchain",
                "tag": "Info",
                "description": "Get block headers within a height range.",
            },
            {
                "name": "Header",
                "operation_id": "header",
                "tag": "Info",
                "description": "Get header at a specified height.",
            },
            {
                "name": "HeaderByHash",
                "operation_id": "header_by_hash",
                "tag": "Info",
                "description": "Get header by hash.",
            },
            {
                "name": "Block",
                "operation_id": "block",
                "tag": "Info",
                "description": "Get block at a specified height.",
            },
            {
                "name": "BlockByHash",
                "operation_id": "block_by_hash",
                "tag": "Info",
                "description": "Get block by hash.",
            },
            {
                "name": "BlockResults",
                "operation_id": "block_results",
                "tag": "Info",
                "description": "Get block results at a specified height.",
            },
            {
                "name": "Commit",
                "operation_id": "commit",
                "tag": "Info",
                "description": "Get commit results at a specified height.",
            },
            {
                "name": "Validators",
                "operation_id": "validators",
                "tag": "Info",
                "description": "Get validator set at a specified height.",
            },
            {"name": "Genesis", "operation_id": "genesis", "tag": "Info", "description": "Get genesis."},
            {
                "name": "GenesisChunked",
                "operation_id": "genesis_chunked",
                "tag": "Info",
                "description": "Get genesis in multiple chunks.",
            },
            {
                "name": "ConsensusParams",
                "operation_id": "consensus_params",
                "tag": "Info",
                "description": "Get consensus parameters.",
            },
            {
                "name": "ConsensusState",
                "operation_id": "consensus_state",
                "tag": "Info",
                "description": "Get consensus state.",
            },
            {
                "name": "DumpConsensusState",
                "operation_id": "dump_consensus_state",
                "tag": "Info",
                "description": "Get consensus state.",
            },
            {
                "name": "UnconfirmedTxs",
                "operation_id": "unconfirmed_txs",
                "tag": "Info",
                "description": "Get the list of unconfirmed transactions.",
            },
            {
                "name": "NumUnconfirmedTxs",
                "operation_id": "num_unconfirmed_txs",
                "tag": "Info",
                "description": "Get data about unconfirmed transactions.",
            },
            {"name": "Tx", "operation_id": "tx", "tag": "Info", "description": "Get transactions by hash."},
            {
                "name": "TxSearch",
                "operation_id": "tx_search",
                "tag": "Info",
                "description": "Search for transactions.",
            },
            {
                "name": "BlockSearch",
                "operation_id": "block_search",
                "tag": "Info",
                "description": "Search for blocks by FinalizeBlock events.",
            },
            {
                "name": "BroadcastEvidence",
                "operation_id": "broadcast_evidence",
                "tag": "Info",
                "description": "Broadcast evidence of misbehavior.",
            },
        ],
    },
    {
        "title": "Transaction Routes",
        "description": (
            "Submission endpoints for broadcasting signed transactions and validating them before inclusion. "
            "Choose async/sync/commit behavior based on how much confirmation you need."
        ),
        "items": [
            {
                "name": "BroadcastTxSync",
                "operation_id": "broadcast_tx_sync",
                "tag": "Tx",
                "description": "Returns with the response from CheckTx. Does not wait for DeliverTx result.",
            },
            {
                "name": "BroadcastTxAsync",
                "operation_id": "broadcast_tx_async",
                "tag": "Tx",
                "description": "Returns right away, with no response. Does not wait for CheckTx nor DeliverTx results.",
            },
            {
                "name": "BroadcastTxCommit",
                "operation_id": "broadcast_tx_commit",
                "tag": "Tx",
                "description": "Returns with the responses from CheckTx and DeliverTx.",
            },
            {
                "name": "CheckTx",
                "operation_id": "check_tx",
                "tag": "Tx",
                "description": "Checks the transaction without executing it.",
            },
        ],
    },
    {
        "title": "ABCI Routes",
        "description": (
            "Application-level endpoints exposed through ABCI. These are useful when you need direct access to "
            "application metadata or state queries beyond generic node status calls."
        ),
        "items": [
            {
                "name": "ABCIInfo",
                "operation_id": "abci_info",
                "tag": "ABCI",
                "description": "Get info about the application.",
            },
            {
                "name": "ABCIQuery",
                "operation_id": "abci_query",
                "tag": "ABCI",
                "description": "Query the application for some information.",
            },
        ],
    },
    {
        "title": "Unsafe Routes",
        "description": (
            "Administrative peer-management endpoints that can change network connectivity at runtime. "
            "They are marked unsafe because exposing them publicly can be abused to manipulate node peering."
        ),
        "items": [
            {
                "name": "DialSeeds",
                "operation_id": "dial_seeds",
                "tag": "Unsafe",
                "description": "Dial seeds (unsafe).",
            },
            {
                "name": "DialPeers",
                "operation_id": "dial_peers",
                "tag": "Unsafe",
                "description": "Add peers or persistent peers (unsafe).",
            },
        ],
    },
]


def api_page() -> rx.Component:
    """API references page."""
    def rpc_card(item: dict[str, str]) -> rx.Component:
        href = f"{RPC_DOCS_BASE}/{item['tag']}/{item['operation_id']}"
        route = f"/{item['operation_id']}"
        return rx.link(
            icon_watermark_hover_card(
                rx.flex(
                    rx.text(
                        route,
                        size="4",
                        weight="bold",
                        color=TEXT_PRIMARY,
                        font_family="'SF Mono', 'Monaco', 'Menlo', monospace",
                    ),
                    direction={"base": "row", "lg": "column"},
                    align={"base": "center", "lg": "start"},
                    spacing="3",
                ),
                rx.text(item["description"], size="3", color=TEXT_MUTED, line_height="1.6"),
                icon="code",
                show_watermark=False,
                padding="1.5rem",
                width="100%",
                cursor="pointer",
            ),
            href=href,
            is_external=True,
            width="100%",
            text_decoration="none",
            _hover={"textDecoration": "none"},
        )

    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("API REFERENCES", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "API References",
                    size="8",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    line_height="1.2",
                ),
                rx.text(
                    "CometBFT RPC is the canonical interface for node status, blocks, validators, "
                    "transactions, and ABCI application state. Use the official CometBFT RPC reference "
                    "for request and response details, then use the list below to scan every available method.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    width="100%",
                ),
                rx.text(
                    "If you are building in Python, many of these routes are already wrapped by the ",
                    rx.link("xian-py", href="https://github.com/xian-technology/xian-py", is_external=True, color=ACCENT),
                    " SDK. "
                    "In those cases, prefer SDK methods for safer defaults and cleaner integration flow instead of calling raw routes directly.",
                    size="3",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    width="100%",
                ),
                spacing="6",
                align_items="start",
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading(
                            "CometBFT RPC Methods",
                            size="6",
                            color=TEXT_PRIMARY,
                            weight="bold",
                        ),
                        section_action_links(
                            [
                                {"label": "RPC Docs", "icon": "book_open", "href": "https://docs.cometbft.com/main/rpc"},
                                {"label": "JSON-RPC Spec", "icon": "scroll_text", "href": "https://docs.cometbft.com/v0.38/spec/rpc/"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "Grouped by category from the CometBFT RPC reference.",
                        size="3",
                        color=TEXT_MUTED,
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    *[
                        subsection(
                            group["title"],
                            rx.text(
                                group["description"],
                                size="3",
                                color=TEXT_MUTED,
                                line_height="1.7",
                                width="100%",
                            ),
                            rx.grid(
                                *[rpc_card(item) for item in group["items"]],
                                columns={"base": "1fr", "md": "repeat(2, minmax(0, 1fr))"},
                                gap="1.5rem",
                                width="100%",
                            ),
                            spacing="4",
                        )
                        for group in RPC_SECTIONS
                    ],
                    spacing="5",
                    width="100%",
                ),
            ),
        ),
    )


__all__ = ["api_page"]
