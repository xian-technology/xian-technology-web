import reflex as rx

from ..components.common import (
    copyable_code_block,
    hover_icon_chip,
    icon_watermark_hover_card,
    linked_heading,
    page_layout,
    section,
    section_action_links,
    section_panel,
    subsection,
    text_with_inline_code,
)
from ..data import BDS_COMPONENTS
from ..state import State, ToolingState
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    BORDER_COLOR,
    CODE_BG,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

SDK_INSTALL_COMMAND = "pip install xian-py"
SDK_WALLET_EXAMPLE = """from xian_py import Wallet

wallet = Wallet()

print(f"Address: {wallet.public_key}")
print(f"Private key: {wallet.private_key}")"""
SDK_BALANCE_EXAMPLE = """from xian_py import Xian, Wallet

wallet = Wallet()
xian = Xian("http://node-ip:26657", wallet=wallet)

balance = xian.get_balance(wallet.public_key)
print(f"Balance: {balance}")"""
SDK_SEND_EXAMPLE = """from xian_py import Xian, Wallet

wallet = Wallet()
xian = Xian("http://node-ip:26657", wallet=wallet)

result = xian.send(amount=10, to_address="recipient_address")
print(f"Transaction successful: {result['success']}")"""
SDK_CONTRACT_EXAMPLE = """from xian_py import Xian, Wallet

wallet = Wallet()
xian = Xian("http://node-ip:26657", wallet=wallet)

result = xian.send_tx(
    contract="currency",
    function="transfer",
    kwargs={"to": "recipient_address", "amount": 100},
)
print(f"Success: {result['success']}")"""
SDK_BDS_STATE_QUERY = """query QueryState {
  allStates(condition: {key: "currency.balances:some_address"}) {
    edges {
      node {
        key
        value
      }
    }
  }
}"""
SDK_BDS_EVENTS_QUERY = """query TransferEventQuery {
  allEvents(
    filter: {dataIndexed: {contains: {to: "some_address"}}}
    condition: {event: "Transfer"}
  ) {
    edges {
      node {
        id
        dataIndexed
        data
        contract
        event
        txHash
      }
    }
  }
}"""
MCP_QUICKSTART = """git clone https://github.com/xian-technology/xian-mcp-server.git
cd xian-mcp-server
docker build -t xian-mcp-server ."""
MCP_CONFIG_SNIPPET = """{
  "mcpServers": {
    "xian": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "xian-mcp-server"]
    }
  }
}"""

SEARCH_SECTIONS = [
    {
        "title": "Tooling to Build and Query",
        "subtitle": "SDKs and data services for contract lifecycles and chain data access.",
        "category": "Technology",
        "badge": "Page",
        "href": "/tooling",
        "keywords": ["Tooling", "SDK", "GraphQL", "BDS"],
    },
    {
        "title": "Python SDK",
        "subtitle": "xian-py for wallets, transactions, and contract workflows.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#python-sdk",
        "keywords": ["xian-py", "SDK", "Wallets", "Transactions"],
    },
    {
        "title": "Xian Linter",
        "subtitle": "Contract linting in inline mode or as a standalone API service.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#xian-linter",
        "keywords": [
            "xian-linter",
            "Linting",
            "Inline mode",
            "Standalone mode",
            "lint_base64",
            "lint_gzip",
            "whitelist_patterns",
        ],
    },
    {
        "title": "Blockchain Data Service (BDS)",
        "subtitle": "PostgreSQL + GraphQL access to transaction and state history.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#blockchain-data-service-bds",
        "keywords": ["BDS", "GraphQL", "PostgreSQL", "PostGraphile"],
    },
    {
        "title": "MCP Server",
        "subtitle": "Local MCP server for AI assistants to interact with Xian wallets, contracts, and the DEX.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#mcp-server",
        "keywords": ["MCP", "AI assistants", "Wallets", "DEX"],
    },
    {
        "title": "Agent Skills",
        "subtitle": "Agent-ready skills for Xian SDK usage and node operations.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#agent-skills",
        "keywords": ["AI skills", "Agents", "xian-py", "Nodes"],
    },
    {
        "title": "AI Guides",
        "subtitle": "AI-ready guides for building and reviewing Xian contracts.",
        "category": "Technology",
        "badge": "Section",
        "href": "/tooling#ai-guides",
        "keywords": ["AI guides", "Contracting guide", "Smart contracts"],
    },
]


def _sdk_install_card() -> rx.Component:
    return icon_watermark_hover_card(
        rx.hstack(
            hover_icon_chip("download"),
            rx.text("Install", size="3", weight="bold", color=TEXT_PRIMARY),
            spacing="3",
            align_items="center",
        ),
        rx.flex(
            rx.text("$", color=ACCENT, weight="bold", size="3"),
            rx.text(
                SDK_INSTALL_COMMAND,
                color=TEXT_PRIMARY,
                size="3",
                font_family="'SF Mono', 'Monaco', monospace",
            ),
            rx.spacer(),
            rx.button(
                rx.box(
                    rx.icon(
                        tag="clipboard_copy",
                        size=18,
                        color="currentColor",
                        opacity=rx.cond(ToolingState.sdk_install_copied, "0", "1"),
                        transform=rx.cond(ToolingState.sdk_install_copied, "scale(0.85)", "scale(1)"),
                        transition="opacity 0.2s ease, transform 0.2s ease",
                        position="absolute",
                        top="0",
                        left="0",
                    ),
                    rx.icon(
                        tag="check",
                        size=18,
                        color="currentColor",
                        opacity=rx.cond(ToolingState.sdk_install_copied, "1", "0"),
                        transform=rx.cond(ToolingState.sdk_install_copied, "scale(1)", "scale(0.85)"),
                        transition="opacity 0.2s ease, transform 0.2s ease",
                        position="absolute",
                        top="0",
                        left="0",
                    ),
                    width="18px",
                    height="18px",
                    position="relative",
                    display="inline-block",
                ),
                on_click=ToolingState.copy_sdk_install_command,
                variant="ghost",
                cursor="pointer",
                padding="0.35rem",
                background_color="transparent",
                color=rx.cond(ToolingState.sdk_install_copied, ACCENT, TEXT_MUTED),
                border="none",
                _hover={"color": ACCENT, "background_color": "transparent"},
                aria_label="Copy install command",
            ),
            gap="0.75rem",
            padding="1rem 1.5rem",
            background=CODE_BG,
            border=f"1px solid {BORDER_COLOR}",
            border_radius="8px",
            align_items="center",
            width="100%",
        ),
        icon="download",
        padding="1.75rem",
    )


def _feature_item(text: str) -> rx.Component:
    return rx.hstack(
        rx.icon(tag="check", size=16, color=ACCENT),
        rx.text(text, size="3", color=TEXT_MUTED),
        spacing="2",
        align_items="center",
    )


def _feature_item_with_code(text: str) -> rx.Component:
    return rx.hstack(
        rx.icon(tag="check", size=16, color=ACCENT),
        text_with_inline_code(
            text,
            size="3",
            color=TEXT_MUTED,
            line_height="1.6",
        ),
        spacing="2",
        align_items="center",
    )


def _tooling_jump_card(
    *,
    title: str,
    description: str,
    target: str,
    icon: str,
) -> rx.Component:
    return rx.link(
        icon_watermark_hover_card(
            rx.hstack(
                hover_icon_chip(icon, size=24),
                rx.heading(title, size="5", weight="bold", color=TEXT_PRIMARY),
                spacing="3",
                align_items="center",
            ),
            rx.text(description, size="3", color=TEXT_MUTED, line_height="1.7"),
            icon=icon,
            padding="1.75rem",
            height="100%",
        ),
        href=f"#{target}",
        width="100%",
        display="block",
        _hover={"textDecoration": "none"},
    )


def tooling_page() -> rx.Component:
    """Tooling and interfaces overview."""
    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("TOOLING", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Tooling to Build and Query",
                    size="8",
                    color=TEXT_PRIMARY,
                    line_height="1.15",
                    weight="bold",
                ),
                rx.text(
                    "SDKs and data services keep builders productive: xian-py for contract lifecycles and BDS for GraphQL access to chain data.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    width="100%",
                ),
                spacing="5",
                align_items="start",
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading("Tool Navigator", size="6", color=TEXT_PRIMARY, weight="bold"),
                    rx.text(
                        "Pick a tooling area and jump to the relevant section below.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                rx.grid(
                    _tooling_jump_card(
                        title="BDS",
                        description="Query chain history and contract state over GraphQL.",
                        target="blockchain-data-service-bds",
                        icon="database",
                    ),
                    _tooling_jump_card(
                        title="Python SDK",
                        description="Build wallet, transaction, and contract workflows with xian-py.",
                        target="python-sdk",
                        icon="code",
                    ),
                    _tooling_jump_card(
                        title="Xian Linter",
                        description="Catch contract and Python issues before deployment.",
                        target="xian-linter",
                        icon="shield",
                    ),
                    _tooling_jump_card(
                        title="MCP Server",
                        description="Expose wallet, contract, and DEX tools to AI assistants.",
                        target="mcp-server",
                        icon="server",
                    ),
                    _tooling_jump_card(
                        title="AI Guides",
                        description="Use machine-readable guidance for safer contract generation and review.",
                        target="ai-guides",
                        icon="book_open",
                    ),
                    _tooling_jump_card(
                        title="Agent Skills",
                        description="Plug skill packs into assistants for SDK and node operations.",
                        target="agent-skills",
                        icon="brain",
                    ),
                    columns={"base": "1", "md": "2", "lg": "3"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading(
                            "Blockchain Data Service (BDS)",
                            anchor_id="blockchain-data-service-bds",
                            size="6",
                            color=TEXT_PRIMARY,
                            weight="bold",
                        ),
                        section_action_links(
                            [
                                {
                                    "label": "Repo",
                                    "icon": "github",
                                    "href": "https://github.com/xian-technology/xian-abci/tree/alter_table/src/xian/services/bds",
                                },
                                {
                                    "label": "DeepWiki",
                                    "icon": "brain",
                                    "href": "https://deepwiki.com/xian-technology/xian-abci/5.3-block-data-service-(bds)",
                                },
                                {"label": "Docs", "icon": "book_open", "href": "https://docs.xian.technology"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "BDS is an optional component of the Python ABCI app. When enabled, it records every transaction into PostgreSQL and exposes that data via a GraphQL API powered by ",
                        rx.link("PostGraphile", href="https://www.graphile.org/postgraphile", is_external=True, color=ACCENT),
                        ".",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.text(
                        "The Schema Guide below summarizes why GraphQL works well for BDS integrations and links directly "
                        "to the machine-readable schema used for query generation and client tooling.",
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
                    *[
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
                            padding="2rem",
                        )
                        for item in BDS_COMPONENTS
                    ],
                    columns={
                        "base": "repeat(1, minmax(0, 1fr))",
                        "md": "repeat(2, minmax(0, 1fr))",
                        "lg": "repeat(3, minmax(0, 1fr))",
                    },
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                rx.vstack(
                    rx.text(
                        "When GraphQL is enabled on a node, the GraphiQL UI is available at the node address under ",
                        rx.el.code(
                            "/graphiql",
                            style={
                                "fontFamily": "'SF Mono', 'Monaco', monospace",
                                "fontSize": "0.9em",
                                "background": CODE_BG,
                                "border": f"1px solid {BORDER_COLOR}",
                                "borderRadius": "6px",
                                "padding": "0.08rem 0.35rem",
                                "color": TEXT_PRIMARY,
                            },
                        ),
                        ". For API access, use ",
                        rx.el.code(
                            "/graphql",
                            style={
                                "fontFamily": "'SF Mono', 'Monaco', monospace",
                                "fontSize": "0.9em",
                                "background": CODE_BG,
                                "border": f"1px solid {BORDER_COLOR}",
                                "borderRadius": "6px",
                                "padding": "0.08rem 0.35rem",
                                "color": TEXT_PRIMARY,
                            },
                        ),
                        ".",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.box(
                        rx.image(
                            src="/postgraphile.png",
                            alt="GraphiQL interface for BDS",
                            width="100%",
                            border_radius="12px",
                            object_fit="cover",
                            box_shadow=f"0 0 18px {ACCENT_SOFT}",
                        ),
                        width="100%",
                        cursor="zoom-in",
                        border_radius="12px",
                        overflow="hidden",
                        on_click=State.open_image_lightbox("/postgraphile.png", "GraphiQL interface for BDS"),
                    ),
                    subsection(
                        "Examples",
                        rx.tabs.root(
                            rx.tabs.list(
                                rx.tabs.trigger("Querying state", value="state", color_scheme="green"),
                                rx.tabs.trigger("Querying events", value="events", color_scheme="green"),
                                gap="0.75rem",
                                wrap="wrap",
                            ),
                        rx.tabs.content(
                                copyable_code_block(
                                    SDK_BDS_STATE_QUERY,
                                    language="graphql",
                                    show_line_numbers=True,
                                    wrap_long_lines=False,
                                    block_margin_top="0.45rem",
                                ),
                                value="state",
                                width="100%",
                            ),
                            rx.tabs.content(
                                rx.vstack(
                                    copyable_code_block(
                                        SDK_BDS_EVENTS_QUERY,
                                        language="graphql",
                                        show_line_numbers=True,
                                        wrap_long_lines=False,
                                        block_margin_top="0.45rem",
                                    ),
                                    rx.text(
                                        "The filter is optional if you want all Transfer events.",
                                        size="3",
                                        color=TEXT_MUTED,
                                        line_height="1.6",
                                    ),
                                    spacing="3",
                                    align_items="start",
                                    width="100%",
                                ),
                                value="events",
                                width="100%",
                            ),
                            default_value="state",
                            width="100%",
                            min_width="0",
                        ),
                        id="bds-examples",
                    ),
                    subsection(
                        "Schema Guide",
                        rx.flex(
                            rx.text(
                                "Use these references to understand GraphQL tradeoffs and build schema-accurate BDS queries.",
                                size="3",
                                color=TEXT_MUTED,
                                line_height="1.7",
                                width="100%",
                            ),
                            section_action_links(
                                [
                                    {
                                        "label": "Repo",
                                        "icon": "github",
                                        "href": "https://github.com/xian-technology/xian-ai-guides/blob/main/bds_graphql_schema.json",
                                    }
                                ]
                            ),
                            direction={"base": "column", "md": "row"},
                            align_items={"base": "start", "md": "center"},
                            justify="between",
                            gap="0.75rem",
                            width="100%",
                        ),
                        rx.grid(
                            icon_watermark_hover_card(
                                rx.hstack(
                                    hover_icon_chip("layers"),
                                    rx.text("Why GraphQL for BDS", size="3", weight="bold", color=TEXT_PRIMARY),
                                    spacing="3",
                                    align_items="center",
                                ),
                                rx.vstack(
                                    _feature_item("Request only needed fields to trim payloads."),
                                    _feature_item("Fetch related state and events in a single query shape."),
                                    _feature_item("Use schema introspection to generate safer typed clients."),
                                    _feature_item("Prototype queries in GraphiQL before wiring app code."),
                                    _feature_item("Reuse stable query patterns across apps and services."),
                                    spacing="2",
                                    align_items="start",
                                ),
                                icon="layers",
                                padding="1.75rem",
                                height="100%",
                            ),
                            icon_watermark_hover_card(
                                rx.hstack(
                                    hover_icon_chip("database"),
                                    rx.text("BDS GraphQL Schema", size="3", weight="bold", color=TEXT_PRIMARY),
                                    spacing="3",
                                    align_items="center",
                                ),
                                rx.vstack(
                                    _feature_item("Look up exact types and fields before writing queries."),
                                    _feature_item("Provide it in prompts for schema-accurate GraphQL output."),
                                    _feature_item("Build dashboard and indexer queries from schema data."),
                                    _feature_item("Cut trial-and-error and runtime query failures."),
                                    _feature_item("Generate typed clients with schema-first planning."),
                                    spacing="2",
                                    align_items="start",
                                ),
                                icon="database",
                                padding="1.75rem",
                                height="100%",
                            ),
                            columns={"base": "1", "lg": "2"},
                            spacing="4",
                            width="100%",
                            align="stretch",
                        ),
                        id="bds-schema-guide",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                    min_width="0",
                ),
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("Python SDK", anchor_id="python-sdk", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [
                                {"label": "Repo", "icon": "github", "href": "https://github.com/xian-technology/xian-py"},
                                {"label": "DeepWiki", "icon": "brain", "href": "https://deepwiki.com/xian-technology/xian-py"},
                                {"label": "Docs", "icon": "book_open", "href": "https://docs.xian.technology"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "xian-py is the Python SDK for interacting with Xian nodes, managing accounts, and deploying or "
                        "calling contracts from scripts and services.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                    ),
                    rx.text(
                        "An SDK gives you a higher-level, well-tested interface so you can build faster with less low-level node plumbing. "
                        "In practice, xian-py helps teams ship safer automation and integrations by standardizing signing, transaction flow, "
                        "and contract interaction patterns.",
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
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("list_checks"),
                            rx.text("Features", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="check", size=16, color=ACCENT),
                                rx.text(
                                    "Create wallets, manage keys, and sign transactions with predictable, reusable helpers.",
                                    size="3",
                                    color=TEXT_MUTED,
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.hstack(
                                rx.icon(tag="check", size=16, color=ACCENT),
                                rx.text(
                                    "Deploy, call, and inspect Python smart contracts from scripts, services, and CI jobs.",
                                    size="3",
                                    color=TEXT_MUTED,
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.hstack(
                                rx.icon(tag="check", size=16, color=ACCENT),
                                rx.text(
                                    "Build, simulate, and submit transactions with clearer feedback and predictable outcomes.",
                                    size="3",
                                    color=TEXT_MUTED,
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.hstack(
                                rx.icon(tag="check", size=16, color=ACCENT),
                                rx.text(
                                    "Query node data, balances, and contract state for backend automation and app integrations.",
                                    size="3",
                                    color=TEXT_MUTED,
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="list_checks",
                        padding="1.75rem",
                    ),
                    _sdk_install_card(),
                    columns={"base": "1", "lg": "1"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Examples",
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Create wallet", value="wallet", color_scheme="green"),
                            rx.tabs.trigger("Get balance", value="balance", color_scheme="green"),
                            rx.tabs.trigger("Send tokens", value="send", color_scheme="green"),
                            rx.tabs.trigger("Call contract", value="contract", color_scheme="green"),
                            gap="0.75rem",
                            wrap="wrap",
                        ),
                        rx.tabs.content(
                            copyable_code_block(
                                SDK_WALLET_EXAMPLE,
                                language="python",
                                show_line_numbers=True,
                                wrap_long_lines=False,
                                block_margin_top="0.45rem",
                            ),
                            value="wallet",
                            width="100%",
                        ),
                        rx.tabs.content(
                            copyable_code_block(
                                SDK_BALANCE_EXAMPLE,
                                language="python",
                                show_line_numbers=True,
                                wrap_long_lines=False,
                                block_margin_top="0.45rem",
                            ),
                            value="balance",
                            width="100%",
                        ),
                        rx.tabs.content(
                            copyable_code_block(
                                SDK_SEND_EXAMPLE,
                                language="python",
                                show_line_numbers=True,
                                wrap_long_lines=False,
                                block_margin_top="0.45rem",
                            ),
                            value="send",
                            width="100%",
                        ),
                        rx.tabs.content(
                            copyable_code_block(
                                SDK_CONTRACT_EXAMPLE,
                                language="python",
                                show_line_numbers=True,
                                wrap_long_lines=False,
                                block_margin_top="0.45rem",
                            ),
                            value="contract",
                            width="100%",
                        ),
                        default_value="wallet",
                        width="100%",
                        min_width="0",
                    ),
                    id="sdk-examples",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("Xian Linter", anchor_id="xian-linter", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [
                                {"label": "Repo", "icon": "github", "href": "https://github.com/xian-technology/xian-linter"},
                                {"label": "DeepWiki", "icon": "brain", "href": "https://deepwiki.com/xian-technology/xian-linter"},
                                {"label": "Docs", "icon": "book_open", "href": "https://pypi.org/project/xian-linter/"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "xian-linter combines PyFlakes with Xian Contracting checks so you can catch Python issues "
                        "and contract-specific violations before deployment.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.text(
                        "Use inline mode for local scripts and CI pipelines, or run the standalone FastAPI mode "
                        "when editors, agents, or backend services need remote linting over HTTP.",
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
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("code", size=24),
                            rx.text("Inline / Programmatic", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _feature_item_with_code("Install with `pip install xian-linter`."),
                            _feature_item_with_code("Run linting directly via `lint_code_inline(contract_code)`."),
                            _feature_item_with_code("Ideal for pre-commit checks, CI gates, and deploy scripts."),
                            _feature_item_with_code("Pass custom `whitelist_patterns` for expected symbols."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="code",
                        padding="1.75rem",
                        height="100%",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("server", size=24),
                            rx.text("Standalone Server", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _feature_item_with_code("Install API extras via `pip install xian-linter[server]`."),
                            _feature_item_with_code("Run with `xian-linter` or `python -m xian_linter`."),
                            _feature_item_with_code("Expose `POST /lint_base64` and `POST /lint_gzip`."),
                            _feature_item_with_code("Use `whitelist_patterns` query param for ignored patterns."),
                            _feature_item_with_code("Returns unified JSON errors with line and column metadata."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="server",
                        padding="1.75rem",
                        height="100%",
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("MCP Server", anchor_id="mcp-server", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [
                                {"label": "Repo", "icon": "github", "href": "https://github.com/xian-technology/xian-mcp-server"},
                                {"label": "DeepWiki", "icon": "brain", "href": "https://deepwiki.com/xian-technology/xian-mcp-server"},
                                {"label": "Docs", "icon": "book_open", "href": "https://modelcontextprotocol.io"},
                            ]
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "A local Model Context Protocol (MCP) server that lets AI assistants create wallets, send transactions, "
                        "query smart contracts, and trade on the Xian DEX through standard MCP tools.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    rx.text(
                        "MCP is an open standard for connecting AI assistants to external tools through a consistent interface. "
                        "Using it here means you can expose Xian capabilities once and reuse them across different assistants, "
                        "reducing custom integration work while improving reliability and portability.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.box(
                    rx.text(
                        "Security note: the MCP server handles private keys and should only be run locally for development.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.6",
                    ),
                    padding="1rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="10px",
                    width="100%",
                ),
                rx.grid(
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("list_checks"),
                            rx.text("Features", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _feature_item("Create or import standard and HD wallets, including BIP39 mnemonic-based flows."),
                            _feature_item("Check balances, send tokens, and simulate transactions before submitting on-chain."),
                            _feature_item("Query contract state, contract source, and token metadata for integrations and audits."),
                            _feature_item("Use DEX helpers for buy and sell workflows with real-time price lookups."),
                            _feature_item("Access crypto utilities for signing, verification, and encryption tasks."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="list_checks",
                        padding="1.75rem",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("terminal"),
                            rx.text("Install & use", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.text(
                            "Clone the repo and build the Docker image locally:",
                            size="3",
                            color=TEXT_MUTED,
                            line_height="1.6",
                        ),
                        copyable_code_block(
                            MCP_QUICKSTART,
                            language="bash",
                            show_line_numbers=False,
                            wrap_long_lines=False,
                        ),
                        rx.text(
                            "Then register the server in your MCP config (Claude Desktop or LM Studio):",
                            size="3",
                            color=TEXT_MUTED,
                            line_height="1.6",
                        ),
                        copyable_code_block(
                            MCP_CONFIG_SNIPPET,
                            language="json",
                            show_line_numbers=False,
                            wrap_long_lines=False,
                        ),
                        icon="terminal",
                        padding="1.75rem",
                    ),
                    columns={"base": "1", "lg": "1"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("AI Guides", anchor_id="ai-guides", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [{"label": "Repo", "icon": "github", "href": "https://github.com/xian-technology/xian-ai-guides"}],
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "AI Guides provide machine-readable references for building with Xian, with the Contracting Guide "
                        "acting as the core rulebook for safe generation, review, and deployment workflows.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.grid(
                    rx.link(
                        icon_watermark_hover_card(
                            rx.hstack(
                                hover_icon_chip("book_open"),
                                rx.text("Contracting Guide", size="3", weight="bold", color=TEXT_PRIMARY),
                                spacing="3",
                                align_items="center",
                            ),
                            rx.vstack(
                                _feature_item("Use it as a policy baseline for allowed imports, decorators, and contract structure."),
                                _feature_item("Attach it to AI prompts so generated code starts from Xian-safe patterns by default."),
                                _feature_item("Review auth checks, state access, and deterministic logic with one shared rule set."),
                                _feature_item("Apply the checklist in PR reviews to catch risky patterns before runtime failures."),
                                _feature_item("Use guide compliance as a release gate to reduce deployment and rollback risk."),
                                spacing="3",
                                align_items="start",
                            ),
                            icon="book_open",
                            padding="1.75rem",
                        ),
                        href="https://github.com/xian-technology/xian-ai-guides/blob/main/contracting-guide.md",
                        is_external=True,
                        width="100%",
                        display="block",
                        _hover={"textDecoration": "none"},
                    ),
                    columns={"base": "1", "lg": "1"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading("Agent Skills", anchor_id="agent-skills", size="6", color=TEXT_PRIMARY, weight="bold"),
                        section_action_links(
                            [{"label": "Repo", "icon": "github", "href": "https://github.com/xian-technology/xian-ai-skills"}],
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "Agent-ready skill packs that teach AI assistants how to build on Xian, operate nodes, and "
                        "work with the core Python tooling.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.grid(
                    rx.link(
                        icon_watermark_hover_card(
                            rx.hstack(
                                hover_icon_chip("code", size=24),
                                rx.heading("xian-sdk-skill", size="5", weight="bold", color=TEXT_PRIMARY),
                                spacing="3",
                                align_items="center",
                            ),
                            rx.text(
                                "Guides agents through xian-py workflows: wallet creation (including HD/BIP39), "
                                "token transfers, contract deployment and calls, state queries, and transaction "
                                "simulation for reliable automation.",
                                size="3",
                                color=TEXT_MUTED,
                                line_height="1.7",
                            ),
                            icon="code",
                            padding="1.75rem",
                            height="100%",
                        ),
                        href="https://github.com/xian-technology/xian-ai-skills/tree/main/xian-sdk-skill",
                        is_external=True,
                        width="100%",
                        display="block",
                        _hover={"textDecoration": "none"},
                    ),
                    rx.link(
                        icon_watermark_hover_card(
                            rx.hstack(
                                hover_icon_chip("server", size=24),
                                rx.heading("xian-node-skill", size="5", weight="bold", color=TEXT_PRIMARY),
                                spacing="3",
                                align_items="center",
                            ),
                            rx.text(
                                "Covers node operations via xian-stack: joining mainnet/testnet, creating networks, "
                                "validator and service node setup, monitoring, CometBFT configuration, and Docker "
                                "deployment basics.",
                                size="3",
                                color=TEXT_MUTED,
                                line_height="1.7",
                            ),
                            icon="server",
                            padding="1.75rem",
                            height="100%",
                        ),
                        href="https://github.com/xian-technology/xian-ai-skills/tree/main/xian-node-skill",
                        is_external=True,
                        width="100%",
                        display="block",
                        _hover={"textDecoration": "none"},
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
    )


__all__ = ["tooling_page"]
