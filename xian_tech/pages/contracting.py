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
)
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    BORDER_COLOR,
    SURFACE,
    TEXT_MUTED,
    TEXT_PRIMARY,
)
ALGORAND_CONTRACT = """import algopy
from algopy import arc4

class Calculator(algopy.ARC4Contract):
    def __init__(self) -> None:
        self.result = algopy.UInt64(0)

    @arc4.abimethod
    def add(self, a: arc4.UInt64, b: arc4.UInt64) -> arc4.UInt64:
        self.result = a.native + b.native
        return arc4.UInt64(self.result)

    @arc4.abimethod
    def read_result(self) -> arc4.UInt64:
        return arc4.UInt64(self.result)
"""

XIAN_CONTRACT = """result = Variable()

@export
def add(a: int, b: int):
    result.set(a + b)

@export
def read_result():
    return result.get()
"""

SOLIDITY_CONTRACT = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.34;

contract Calculator {
    uint256 public result;

    function add(uint256 a, uint256 b) external {
        result = a + b;
    }

    function readResult() external view returns (uint256) {
        return result;
    }
}
"""

VYPER_CONTRACT = """#pragma version ~=0.4.0
result: public(uint256)

@external
def add(a: uint256, b: uint256):
    self.result = a + b

@external
@view
def read_result() -> uint256:
    return self.result
"""

MOVE_CONTRACT = """module 0x42::calculator {
    use std::signer;

    struct Result has key {
        value: u64,
    }

    public entry fun init(account: &signer) {
        move_to(account, Result { value: 0 });
    }

    public entry fun add(account: &signer, a: u64, b: u64) acquires Result {
        let addr = signer::address_of(account);
        let result = borrow_global_mut<Result>(addr);
        result.value = a + b;
    }

    public fun read_result(account: address): u64 acquires Result {
        borrow_global<Result>(account).value
    }
}
"""

TACT_CONTRACT = """message Add {
    a: Int as uint64;
    b: Int as uint64;
}

contract Calculator {
    result: Int as uint64 = 0;

    receive(msg: Add) {
        self.result = msg.a + msg.b;
    }

    get fun readResult(): Int {
        return self.result;
    }
}
"""

ANCHOR_CONTRACT = """use anchor_lang::prelude::*;

declare_id!("11111111111111111111111111111111");

#[program]
pub mod calculator {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        ctx.accounts.calculator.result = 0;
        Ok(())
    }

    pub fn add(ctx: Context<Update>, a: u64, b: u64) -> Result<()> {
        ctx.accounts.calculator.result = a.saturating_add(b);
        Ok(())
    }
}

#[account]
pub struct CalculatorAccount {
    pub result: u64,
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = signer, space = 8 + 8)]
    pub calculator: Account<'info, CalculatorAccount>,
    #[account(mut)]
    pub signer: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(mut)]
    pub calculator: Account<'info, CalculatorAccount>,
}
"""

CONTRACT_EXAMPLES = [
    {
        "label": "Xian",
        "value": "xian",
        "language": "python",
        "code": XIAN_CONTRACT,
        "diagram_src": "/flows/xian_flow.svg",
    },
    {
        "label": "Algorand Python",
        "value": "algorand_python",
        "language": "python",
        "code": ALGORAND_CONTRACT,
        "diagram_src": "/flows/algorand_python_flow.svg",
    },
    {
        "label": "Solidity",
        "value": "solidity",
        "language": "solidity",
        "code": SOLIDITY_CONTRACT,
        "diagram_src": "/flows/solidity_flow.svg",
    },
    {
        "label": "Vyper",
        "value": "vyper",
        "language": "python",
        "code": VYPER_CONTRACT,
        "diagram_src": "/flows/vyper_flow.svg",
    },
    {
        "label": "Move",
        "value": "move",
        "language": "rust",
        "code": MOVE_CONTRACT,
        "diagram_src": "/flows/move_flow.svg",
    },
    {
        "label": "TON (Tact)",
        "value": "ton_tact",
        "language": "solidity",
        "code": TACT_CONTRACT,
        "diagram_src": "/flows/ton_tact_flow.svg",
    },
    {
        "label": "Rust (Anchor)",
        "value": "rust_anchor",
        "language": "rust",
        "code": ANCHOR_CONTRACT,
        "diagram_src": "/flows/rust_anchor_flow.svg",
    },
]

HIGHLIGHTS = [
    {
        "title": "Python-first by design",
        "icon": "code",
        "body": (
            "No custom DSLs or transpilers. Contracts are idiomatic Python, making audits and upgrades straightforward "
            "and letting teams use the language they already know."
        ),
        "detail": (
            "Execution stays on the standard Python VM end to end, so there is no translation layer where semantics can drift "
            "or opaque behavior can creep in."
        ),
    },
    {
        "title": "Native value semantics",
        "icon": "scale",
        "body": (
            "We avoid bespoke integer abstractions for balances. The engine stays Python-native rather than inventing "
            "a special-purpose blockchain language."
        ),
        "detail": (
            "Decimal-friendly value types keep amounts natural to read and reason about. Solidity-style integer scaling forces "
            "manual conversions and can still introduce precision pitfalls."
        ),
    },
    {
        "title": "Deterministic fees",
        "icon": "calculator",
        "body": (
            "Fees are deterministic and compute-based, so outcomes and costs can be simulated before a transaction is sent."
        ),
        "detail": (
            "Chi maps directly to the computation required for contract execution. A dry run yields both the expected result "
            "and the exact fee, so you can verify the outcome or opt out before spending."
        ),
    },
    {
        "title": "Standalone & portable",
        "icon": "plug",
        "body": (
            "The contracting library can run independently and could integrate with other node systems—not just CometBFT—"
            "or power entirely different use cases."
        ),
        "detail": (
            "You can embed the engine inside a local app, test harness, or other runtime. Blockchain integration is a choice, "
            "not a requirement."
        ),
    },
    {
        "title": "Upgradable patterns",
        "icon": "puzzle",
        "body": (
            "With the right design patterns, you can ship upgradable contracts when you need them—without forcing "
            "complexity on contracts that don't."
        ),
        "detail": (
            "Contracts can call other contracts, and routing through a registry lets you swap implementations. Bind that switch "
            "to a multisig so upgrades only happen with explicit consensus."
        ),
    },
    {
        "title": "Event-driven observability",
        "icon": "activity",
        "body": (
            "Contracts emit structured, typed events so external systems can track state changes without polling."
        ),
        "detail": (
            "Index by sender, receiver, or any custom field to power real-time dashboards, analytics, or reactive workflows "
            "that respond to contract activity."
        ),
    },
]

WHY_IT_MATTERS = [
    {
        "title": "One Runtime, Fewer Moving Parts",
        "icon": "layers",
        "body": (
            "No extra compiler is required in the core authoring path. If you already have Python, "
            "you already have what you need to write and reason about contracts."
        ),
        "detail": (
            "Reducing toolchain depth lowers setup friction and avoids avoidable build-step failures in local and CI workflows."
        ),
    },
    {
        "title": "Audit What Actually Runs",
        "icon": "check",
        "body": (
            "The code developers review is expressed in the same language that executes. "
            "There is no hidden source-to-bytecode language switch in between."
        ),
        "detail": (
            "Fewer translation boundaries means fewer places for semantic mismatch, edge-case compiler behavior, "
            "or opaque transformations to hide."
        ),
    },
    {
        "title": "Smaller Failure Surface",
        "icon": "triangle_alert",
        "body": (
            "Every additional compiler, transpiler, or plugin introduces another component that can fail, "
            "drift in version, or break compatibility."
        ),
        "detail": (
            "A shorter execution pipeline reduces integration risk and shrinks the number of things operators must keep healthy."
        ),
    },
    {
        "title": "Faster Team Onboarding",
        "icon": "book_open",
        "body": (
            "Python teams can become productive quickly without first mastering a specialized compilation stack "
            "just to ship basic contract logic."
        ),
        "detail": (
            "Less time is spent wiring tooling and more time is spent on domain logic, tests, and security review."
        ),
    },
    {
        "title": "Simpler Ops and Release Flow",
        "icon": "gauge",
        "body": (
            "Fewer required toolchains simplify reproducibility across developer machines, CI pipelines, "
            "and production release processes."
        ),
        "detail": (
            "When the deployment path is shorter, upgrades and incident response become easier to operate and verify."
        ),
    },
    {
        "title": "Clearer Debugging and Triage",
        "icon": "list_checks",
        "body": (
            "Debugging stays within one language model, which makes stack traces, contract behavior, "
            "and review conversations easier to follow."
        ),
        "detail": (
            "That clarity helps teams find issues faster and lowers the cognitive load during high-pressure fixes."
        ),
    },
]

SEARCH_SECTIONS = [
    {
        "title": "Pure Python Smart Contracts",
        "subtitle": "Deterministic, chi-metered execution with native Python contracts.",
        "category": "Technology",
        "badge": "Page",
        "href": "/contracting",
        "keywords": ["Python", "Contracts", "Deterministic", "Smart contracts"],
    },
    *[
        {
            "title": item["title"],
            "subtitle": item["body"],
            "category": "Technology",
            "badge": "Highlight",
            "href": "/contracting",
            "keywords": [item["title"]],
        }
        for item in HIGHLIGHTS
    ],
    {
        "title": "Compare Contracting Platforms",
        "subtitle": (
            "Side-by-side examples across Xian, Algorand Python, Solidity, Vyper, "
            "Move, TON (Tact), and Rust (Anchor)."
        ),
        "category": "Technology",
        "badge": "Comparison",
        "href": "/contracting",
        "keywords": [
            "Comparison",
            "Xian",
            "Algorand Python",
            "Solidity",
            "Vyper",
            "Move",
            "TON",
            "Tact",
            "Rust",
            "Anchor",
        ],
    },
    {
        "title": "Benefits of the Xian Approach",
        "subtitle": "Why the Xian direct-Python execution model reduces stack complexity and risk.",
        "category": "Technology",
        "badge": "Section",
        "href": "/contracting",
        "keywords": ["No compiler", "Python runtime", "Simplicity", "Reliability", "Auditability"],
    },
]


def contracting_page() -> rx.Component:
    """Python smart contract engine overview."""
    def choice_card(title: str, body: str, detail: str, icon: str) -> rx.Component:
        return icon_watermark_hover_card(
            rx.flex(
                hover_icon_chip(icon),
                rx.heading(title, size="5", weight="bold", color=TEXT_PRIMARY),
                direction={"base": "row", "lg": "column"},
                align={"base": "center", "lg": "start"},
                spacing="3",
            ),
            rx.text(body, size="3", color=TEXT_MUTED, line_height="1.7"),
            rx.text(detail, size="2", color=TEXT_MUTED, line_height="1.6"),
            icon=icon,
            padding="2rem",
        )

    def guide_point(text: str) -> rx.Component:
        return rx.hstack(
            rx.icon(tag="check", size=16, color=ACCENT),
            rx.text(text, size="3", color=TEXT_MUTED, line_height="1.6"),
            spacing="2",
            align_items="center",
        )

    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("CONTRACTING", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Pure Python Smart Contracts",
                    size="8",
                    color=TEXT_PRIMARY,
                    line_height="1.15",
                    weight="bold",
                ),
                rx.text(
                    "The heart of Xian is a native Python contracting engine—no transpilers, no second-class runtimes. Deterministic, chi-metered execution keeps performance predictable while making audits and upgrades straightforward.",
                    size="4",
                    color=TEXT_MUTED,
                    width="100%",
                    line_height="1.7",
                ),
                spacing="5",
                align_items="start",
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                        rx.flex(
                            linked_heading("Contracting Engine", size="6", color=TEXT_PRIMARY, weight="bold"),
                            section_action_links(
                                [
                                    {
                                        "label": "Repo",
                                        "icon": "github",
                                        "href": "https://github.com/xian-technology/xian-contracting",
                                    },
                                    {
                                        "label": "DeepWiki",
                                        "icon": "brain",
                                        "href": "https://deepwiki.com/xian-technology/xian-contracting",
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
                            "The contracting engine executes pure Python contracts with deterministic rules and a chi-metered "
                            "budget. It keeps developer ergonomics high without compromising on predictable execution.",
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
                        choice_card(item["title"], item["body"], item["detail"], item["icon"])
                        for item in HIGHLIGHTS
                    ],
                    columns={"base": "repeat(1, minmax(0, 1fr))", "lg": "repeat(3, minmax(0, 1fr))"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Compare Contracting Platforms",
                    rx.text(
                        "Let’s compare a simple add-and-read contract across stacks: Algorand started from TEAL "
                        "(assembly-like), then introduced PyTeal, and now offers Algorand Python workflows, but contracts "
                        "still compile to AVM artifacts before runtime. On Ethereum, Solidity remains the dominant language "
                        "while Vyper emerged as a Pythonic EVM alternative; both still compile to bytecode. Move, TON/Tact, "
                        "and Rust/Anchor also rely on explicit compile-and-deploy pipelines and more specialized blockchain "
                        "abstractions, which are often less straightforward for developers without direct blockchain experience. "
                        "Xian’s core difference is a shorter path: contracts execute directly in the Python runtime (VM) "
                        "without an additional source-language compiler stage.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                    ),
                    spacing="2",
                    heading_size="5",
                    margin_top="2rem",
                ),
                rx.tabs.root(
                    rx.tabs.list(
                        *[
                            rx.tabs.trigger(
                                example["label"],
                                value=example["value"],
                                color_scheme="green",
                            )
                            for example in CONTRACT_EXAMPLES
                        ],
                        gap="0.75rem",
                        wrap="wrap",
                    ),
                    *[
                        rx.tabs.content(
                            rx.vstack(
                                copyable_code_block(
                                    example["code"],
                                    language=example["language"],
                                    show_line_numbers=True,
                                    wrap_long_lines=False,
                                    block_margin_top="0.45rem",
                                ),
                                subsection(
                                    "Execution Flow",
                                    rx.image(
                                        src=example["diagram_src"],
                                        alt=f"{example['label']} execution flow diagram",
                                        width="100%",
                                    ),
                                    heading_size="4",
                                    spacing="3",
                                    margin_top="1.25rem",
                                ),
                                spacing="3",
                                align_items="start",
                                width="100%",
                            ),
                            value=example["value"],
                            width="100%",
                        )
                        for example in CONTRACT_EXAMPLES
                    ],
                    default_value=CONTRACT_EXAMPLES[0]["value"],
                    width="100%",
                    min_width="0",
                ),
                subsection(
                    "Benefits of the Xian Approach",
                    rx.text(
                        "This approach is valuable because it removes avoidable complexity from the contract path. "
                        "When execution stays in Python end to end, teams spend less energy on compiler plumbing and "
                        "more on contract correctness, testing, and security.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.7",
                    ),
                    spacing="3",
                    heading_size="5",
                    margin_top="2rem",
                ),
                rx.grid(
                    *[
                        choice_card(item["title"], item["body"], item["detail"], item["icon"])
                        for item in WHY_IT_MATTERS
                    ],
                    columns={"base": "repeat(1, minmax(0, 1fr))", "lg": "repeat(3, minmax(0, 1fr))"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            ),
        ),
        section(
            section_panel(
                rx.vstack(
                        rx.flex(
                            linked_heading("Contracting AI Guide", size="6", color=TEXT_PRIMARY, weight="bold"),
                            section_action_links(
                                [
                                    {
                                        "label": "Repo",
                                        "icon": "github",
                                        "href": "https://github.com/xian-technology/xian-ai-guides/blob/main/contracting-guide.md",
                                    }
                                ]
                            ),
                            direction={"base": "column", "md": "row"},
                            align_items={"base": "start", "md": "center"},
                            justify="between",
                            gap="0.75rem",
                            width="100%",
                        ),
                        rx.text(
                            "The Contracting AI Guide is the operational spec for AI-assisted Xian contract development. "
                            "It converts platform constraints into explicit authoring and review rules so generated contracts stay valid, deterministic, and deployable.",
                            size="3",
                            color=TEXT_MUTED,
                            line_height="1.7",
                            width="100%",
                        ),
                        rx.text(
                            "Used early during prompt design and again during review, it reduces invalid output, shortens iteration cycles, "
                            "and gives teams a consistent quality bar across engineers and AI workflows.",
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
                            hover_icon_chip("shield"),
                            rx.text("Why this guide matters", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.text(
                            "The guide reduces uncertainty in AI-generated contract code and makes review criteria explicit.",
                            size="3",
                            color=TEXT_MUTED,
                            line_height="1.6",
                        ),
                        rx.vstack(
                            guide_point("Catches rule violations before deploy review."),
                            guide_point("Keeps AI output deterministic and policy-aligned."),
                            guide_point("Standardizes review criteria across teams."),
                            guide_point("Reduces rework with a clear quality baseline."),
                            guide_point("Improves predictability in CI and audits."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="shield",
                        padding="1.75rem",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("list_checks"),
                            rx.text("How to use it in practice", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.text(
                            "Treat the guide as both generation context and a review checklist in your contract workflow.",
                            size="3",
                            color=TEXT_MUTED,
                            line_height="1.6",
                        ),
                        rx.vstack(
                            guide_point("Load guide context before generating contract code."),
                            guide_point("Require allowed decorators, state primitives, and imports."),
                            guide_point("Validate signatures, state access, and auth logic."),
                            guide_point("Run dry-runs/tests and reject rule-violating output."),
                            guide_point("Reuse the same checklist in every PR review."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="list_checks",
                        padding="1.75rem",
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            ),
        ),
    )


__all__ = ["contracting_page"]
