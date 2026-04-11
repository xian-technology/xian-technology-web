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
from ..theme import (
    ACCENT,
    ACCENT_GLOW,
    ACCENT_SOFT,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

SEARCH_SECTIONS = [
    {
        "id": "tutorials-page",
        "title": "Contract Tutorials",
        "subtitle": "Scenario-based guides for writing contracts on Xian.",
        "category": "Developers",
        "badge": "Page",
        "href": "/tutorials",
        "keywords": ["Tutorials", "Contracts", "Guides", "Developers"],
    },
    {
        "id": "tutorials-store-data",
        "title": "Scenario: Store Data On Chain",
        "subtitle": "Initialize state, save values, and read them back.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/tutorials#scenario-store-data",
        "keywords": ["Variable", "Hash", "save", "read", "seed"],
    },
    {
        "id": "tutorials-token",
        "title": "Scenario: Token From Scratch",
        "subtitle": "Derive a minimal token implementation from XSC0001.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/tutorials#scenario-token-from-scratch",
        "keywords": ["token", "XSC0001", "transfer", "approve", "transfer_from"],
    },
    {
        "id": "tutorials-multisig",
        "title": "Scenario: Multisig Contract",
        "subtitle": "Propose, approve, and execute treasury transfers with threshold control.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/tutorials#scenario-multisig",
        "keywords": ["multisig", "treasury", "owners", "threshold", "approvals"],
    },
    {
        "id": "tutorials-upgradable",
        "title": "Scenario: Upgradable Router",
        "subtitle": "Call one implementation contract and switch targets safely.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/tutorials#scenario-upgradable-contracts",
        "keywords": ["upgrade", "router", "importlib", "proxy", "implementation"],
    },
]

# Scenario 1: store data on chain.
STORE_DATA_STEP_1 = '''# Persistent contract state.
records = Hash(default_value='')'''

STORE_DATA_STEP_2 = '''# Saves or overwrites a value by key.
@export
def save(key: str, value: str):
    assert len(key) > 0, 'key required'
    records[key] = value'''

STORE_DATA_STEP_3 = '''# Reads the current value for a key.
@export
def read(key: str):
    return records[key]'''

STORE_DATA_FULL = '''# Stage 1: Declare persistent state.
records = Hash(default_value='')

# Stage 2: Write path.
@export
def save(key: str, value: str):
    assert len(key) > 0, 'key required'
    records[key] = value

# Stage 3: Read path.
@export
def read(key: str):
    return records[key]'''

# Scenario 2: token from scratch (XSC0001 derived).
TOKEN_STEP_1 = '''# Core token storage.
balances = Hash(default_value=0)
approvals = Hash(default_value=0)
metadata = Hash()'''

TOKEN_STEP_2 = '''# Initialize token metadata and initial supply.
@construct
def seed():
    metadata['token_name'] = 'Tutorial Token'
    metadata['token_symbol'] = 'TUT'
    metadata['token_logo_url'] = ''
    metadata['token_website'] = ''
    # Operator governs privileged metadata changes.
    metadata['operator'] = ctx.caller
    # Mint initial supply to deployer.
    balances[ctx.caller] = 1_000_000'''

TOKEN_STEP_3 = '''# Standard read endpoint.
@export
def balance_of(account: str):
    return balances[account]

# Direct transfer between holders.
@export
def transfer(amount: float, to: str):
    assert amount > 0, 'amount must be positive'
    assert balances[ctx.caller] >= amount, 'insufficient funds'
    balances[ctx.caller] -= amount
    balances[to] += amount'''

TOKEN_STEP_4 = '''# Allow another address/contract to spend on your behalf.
@export
def approve(amount: float, to: str):
    assert amount >= 0, 'amount must be non-negative'
    approvals[ctx.caller, to] = amount

# Spend from `main_account` using allowance.
@export
def transfer_from(amount: float, to: str, main_account: str):
    assert amount > 0, 'amount must be positive'
    assert approvals[main_account, ctx.caller] >= amount, 'not approved'
    assert balances[main_account] >= amount, 'insufficient funds'
    # Consume allowance before moving funds.
    approvals[main_account, ctx.caller] -= amount
    balances[main_account] -= amount
    balances[to] += amount'''

TOKEN_STEP_5 = '''# Restricted metadata updates for operator/governance.
@export
def change_metadata(key: str, value):
    assert ctx.caller == metadata['operator'], 'operator only'
    metadata[key] = value'''

TOKEN_FULL = '''# Stage 1: Core token storage.
balances = Hash(default_value=0)
approvals = Hash(default_value=0)
metadata = Hash()

# Stage 2: Initialize metadata and supply.
@construct
def seed():
    metadata['token_name'] = 'Tutorial Token'
    metadata['token_symbol'] = 'TUT'
    metadata['token_logo_url'] = ''
    metadata['token_website'] = ''
    # Operator governs privileged metadata changes.
    metadata['operator'] = ctx.caller
    # Mint initial supply to deployer.
    balances[ctx.caller] = 1_000_000

# Stage 3: Read holder balance.
@export
def balance_of(account: str):
    return balances[account]

# Stage 4: Direct transfers.
@export
def transfer(amount: float, to: str):
    assert amount > 0, 'amount must be positive'
    assert balances[ctx.caller] >= amount, 'insufficient funds'
    balances[ctx.caller] -= amount
    balances[to] += amount

# Stage 5: Grant delegated spending allowance.
@export
def approve(amount: float, to: str):
    assert amount >= 0, 'amount must be non-negative'
    approvals[ctx.caller, to] = amount

# Stage 6: Spend via allowance.
@export
def transfer_from(amount: float, to: str, main_account: str):
    assert amount > 0, 'amount must be positive'
    assert approvals[main_account, ctx.caller] >= amount, 'not approved'
    assert balances[main_account] >= amount, 'insufficient funds'
    # Consume allowance before moving funds.
    approvals[main_account, ctx.caller] -= amount
    balances[main_account] -= amount
    balances[to] += amount

# Stage 7: Operator-managed metadata changes.
@export
def change_metadata(key: str, value):
    assert ctx.caller == metadata['operator'], 'operator only'
    metadata[key] = value'''

# Scenario 3: multisig.
MULTISIG_STEP_1 = '''# Core multisig state.
owners = Hash(default_value=False)
required_approvals = Variable()
proposal_count = Variable()
proposals = Hash(default_value=None)
approvals = Hash(default_value=False)
approval_totals = Hash(default_value=0)'''

MULTISIG_STEP_2 = '''# Configure owners and approval threshold at deployment.
@construct
def seed(owner_a: str, owner_b: str, owner_c: str, required: int = 2):
    assert required >= 2, 'required must be >= 2'
    owners[owner_a] = True
    owners[owner_b] = True
    owners[owner_c] = True
    required_approvals.set(required)
    proposal_count.set(0)'''

MULTISIG_STEP_3 = '''# Create a transfer proposal and auto-approve by proposer.
@export
def propose_transfer(token_contract: str, to: str, amount: float):
    assert_owner()
    assert amount > 0, 'amount must be positive'

    # Allocate sequential proposal IDs.
    proposal_id = proposal_count.get()
    proposal_count.set(proposal_id + 1)

    proposals[proposal_id] = {
        'token_contract': token_contract,
        'to': to,
        'amount': amount,
        'executed': False,
    }

    approvals[proposal_id, ctx.caller] = True
    approval_totals[proposal_id] = 1
    return proposal_id'''

MULTISIG_STEP_4 = '''# Add one owner approval and execute when threshold is reached.
@export
def approve_transfer(proposal_id: int):
    assert_owner()
    proposal = proposals[proposal_id]
    assert proposal is not None, 'unknown proposal'
    assert proposal['executed'] is False, 'already executed'
    assert approvals[proposal_id, ctx.caller] is False, 'already approved'

    approvals[proposal_id, ctx.caller] = True
    approval_totals[proposal_id] += 1

    # Execute immediately once threshold is reached.
    if approval_totals[proposal_id] >= required_approvals.get():
        execute_transfer(proposal_id)'''

MULTISIG_STEP_5 = '''# Internal execution step that performs the token transfer.
def execute_transfer(proposal_id: int):
    proposal = proposals[proposal_id]
    # `importlib` is injected by Contracting runtime.
    token = importlib.import_module(proposal['token_contract'])
    token.transfer(amount=proposal['amount'], to=proposal['to'])

    proposal['executed'] = True
    proposals[proposal_id] = proposal'''

MULTISIG_FULL = '''# Stage 1: Core multisig state.
owners = Hash(default_value=False)
required_approvals = Variable()
proposal_count = Variable()
proposals = Hash(default_value=None)
approvals = Hash(default_value=False)
approval_totals = Hash(default_value=0)

# Stage 2: Shared owner check.
def assert_owner():
    assert owners[ctx.caller], 'owner only'

# Stage 3: Configure owners and threshold.
@construct
def seed(owner_a: str, owner_b: str, owner_c: str, required: int = 2):
    assert required >= 2, 'required must be >= 2'
    owners[owner_a] = True
    owners[owner_b] = True
    owners[owner_c] = True
    required_approvals.set(required)
    proposal_count.set(0)

# Stage 4: Propose transfer.
@export
def propose_transfer(token_contract: str, to: str, amount: float):
    assert_owner()
    assert amount > 0, 'amount must be positive'

    # Allocate sequential proposal IDs.
    proposal_id = proposal_count.get()
    proposal_count.set(proposal_id + 1)

    proposals[proposal_id] = {
        'token_contract': token_contract,
        'to': to,
        'amount': amount,
        'executed': False,
    }

    approvals[proposal_id, ctx.caller] = True
    approval_totals[proposal_id] = 1
    return proposal_id

# Stage 5: Approve and auto-execute on threshold.
@export
def approve_transfer(proposal_id: int):
    assert_owner()
    proposal = proposals[proposal_id]
    assert proposal is not None, 'unknown proposal'
    assert proposal['executed'] is False, 'already executed'
    assert approvals[proposal_id, ctx.caller] is False, 'already approved'

    approvals[proposal_id, ctx.caller] = True
    approval_totals[proposal_id] += 1

    # Execute immediately once threshold is reached.
    if approval_totals[proposal_id] >= required_approvals.get():
        execute_transfer(proposal_id)

# Stage 6: Execute transfer from this contract balance.
def execute_transfer(proposal_id: int):
    proposal = proposals[proposal_id]
    # `importlib` is injected by Contracting runtime.
    token = importlib.import_module(proposal['token_contract'])
    token.transfer(amount=proposal['amount'], to=proposal['to'])

    proposal['executed'] = True
    proposals[proposal_id] = proposal

# Optional read helper for clients/UI.
@export
def get_proposal(proposal_id: int):
    return proposals[proposal_id]'''

# Scenario 4: upgradable router.
UPGRADE_V1 = '''# Implementation v1 state.
count = Variable()

# Initialize v1 storage.
@construct
def seed():
    count.set(0)

# v1 behavior: increment by provided step.
@export
def increment(step: int = 1):
    count.set(count.get() + step)
    return count.get()

# Return current value.
@export
def current():
    return count.get()'''

UPGRADE_V2 = '''# Implementation v2 state.
count = Variable()

# Initialize v2 storage.
@construct
def seed():
    count.set(0)

# v2 behavior: same interface, different logic.
@export
def increment(step: int = 1):
    count.set(count.get() + (step * 2))
    return count.get()

# Return current value.
@export
def current():
    return count.get()'''

UPGRADE_ROUTER_STEP_1 = '''# Router state: admin + active implementation target.
admin = Variable()
active_contract = Variable()'''

UPGRADE_ROUTER_STEP_2 = '''# Set initial implementation at deployment.
@construct
def seed(initial_contract: str = 'con_counter_v1'):
    admin.set(ctx.caller)
    active_contract.set(initial_contract)'''

UPGRADE_ROUTER_STEP_3 = '''# Forward write calls to the active implementation.
@export
def increment(step: int = 1):
    # `importlib` is injected by Contracting runtime.
    target = importlib.import_module(active_contract.get())
    return target.increment(step=step)

# Forward read calls to the active implementation.
@export
def current():
    # `importlib` is injected by Contracting runtime.
    target = importlib.import_module(active_contract.get())
    return target.current()'''

UPGRADE_ROUTER_STEP_4 = '''# Admin-only upgrade switch.
@export
def set_active_contract(contract: str):
    assert ctx.caller == admin.get(), 'admin only'
    active_contract.set(contract)'''

UPGRADE_ROUTER_STEP_5 = '''# Visibility helper for clients and tooling.
@export
def get_active_contract():
    return active_contract.get()'''

UPGRADE_ROUTER_FULL = '''# Stage 1: Router state.
admin = Variable()
active_contract = Variable()

# Stage 2: Initialize with v1 target.
@construct
def seed(initial_contract: str = 'con_counter_v1'):
    admin.set(ctx.caller)
    active_contract.set(initial_contract)

# Stage 3: Forward write calls to active target.
@export
def increment(step: int = 1):
    # `importlib` is injected by Contracting runtime.
    target = importlib.import_module(active_contract.get())
    return target.increment(step=step)

# Stage 4: Forward read calls to active target.
@export
def current():
    # `importlib` is injected by Contracting runtime.
    target = importlib.import_module(active_contract.get())
    return target.current()

# Stage 5: Admin-controlled implementation switch.
@export
def set_active_contract(contract: str):
    assert ctx.caller == admin.get(), 'admin only'
    active_contract.set(contract)

# Stage 6: Expose active implementation.
@export
def get_active_contract():
    return active_contract.get()'''

UPGRADE_CALL_FLOW = '''# 1) Deploy contracts:
#    - con_counter_v1
#    - con_counter_v2
#    - con_counter_router (seed with initial_contract='con_counter_v1')

# 2) Calls initially route to v1 logic.
xian.send_tx('con_counter_router', 'increment', {'step': 1})
xian.send_tx('con_counter_router', 'current', {})

# 3) Switch router target to v2.
xian.send_tx(
    'con_counter_router',
    'set_active_contract',
    {'contract': 'con_counter_v2'},
)

# 4) Calls now route to v2 logic without changing router address.
xian.send_tx('con_counter_router', 'increment', {'step': 1})
xian.send_tx('con_counter_router', 'current', {})'''


def _scenario_jump_card(
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
            rx.text(
                description,
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
                width="100%",
            ),
            icon=icon,
            padding="1.75rem",
            height="100%",
        ),
        href=f"#{target}",
        width="100%",
        display="block",
        _hover={"textDecoration": "none"},
    )


def _tutorial_step(
    step: int,
    title: str,
    *,
    why: str,
    how: str,
    snippet: str | None = None,
    language: str = "python",
) -> rx.Component:
    blocks = [
        rx.hstack(
            rx.box(
                rx.text(str(step), size="2", weight="bold", color=ACCENT),
                min_width="1.5rem",
                height="1.5rem",
                display="inline-flex",
                align_items="center",
                justify_content="center",
                background=ACCENT_SOFT,
                border=f"1px solid {ACCENT_GLOW}",
                border_radius="999px",
            ),
            rx.heading(title, size="5", weight="bold", color=TEXT_PRIMARY),
            spacing="3",
            align_items="center",
            width="100%",
        ),
        rx.vstack(
            rx.text("Why", size="2", weight="bold", color=ACCENT),
            text_with_inline_code(
                why,
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
                width="100%",
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        rx.vstack(
            rx.text("How", size="2", weight="bold", color=ACCENT),
            text_with_inline_code(
                how,
                size="3",
                color=TEXT_MUTED,
                line_height="1.7",
                width="100%",
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
    ]

    if snippet:
        blocks.append(
            copyable_code_block(
                snippet,
                language=language,
                show_line_numbers=False,
                wrap_long_lines=False,
            )
        )

    return rx.box(
        rx.vstack(
            *blocks,
            spacing="3",
            align_items="start",
            width="100%",
        ),
        width="100%",
        border=f"1px solid {ACCENT_GLOW}",
        border_radius="12px",
        background=rx.color_mode_cond(
            light="rgba(22, 163, 74, 0.035)",
            dark="rgba(34, 197, 94, 0.06)",
        ),
        padding=rx.breakpoints(initial="1rem", md="1.15rem", lg="1.25rem"),
    )


def tutorials_page() -> rx.Component:
    """Scenario-first tutorials for common Xian contract patterns."""
    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("TUTORIALS", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Contract Tutorials",
                    size="8",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    line_height="1.2",
                ),
                rx.text(
                    "Learn by building four practical patterns: data storage, token design from standard requirements, "
                    "multisig treasury controls, and an upgradable router flow for contract-to-contract calls.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
                    width="100%",
                ),
                rx.box(
                    rx.hstack(
                        rx.icon(tag="triangle_alert", size=18, color=ACCENT),
                        rx.hstack(
                            rx.text(
                                "Before diving into these tutorials, make sure you understand the basics of Xian contracting.",
                                size="3",
                                color=TEXT_MUTED,
                                line_height="1.6",
                            ),
                            rx.link(
                                rx.hstack(
                                    rx.icon(tag="book_open", size=16),
                                    rx.text("Read the contracting docs", size="3"),
                                    spacing="2",
                                    align_items="center",
                                ),
                                href="https://docs.xian.technology",
                                is_external=True,
                                color=ACCENT,
                                _hover={"textDecoration": "underline"},
                            ),
                            spacing="2",
                            align_items="center",
                            wrap="wrap",
                            width="100%",
                        ),
                        spacing="2",
                        align_items="center",
                        width="100%",
                    ),
                    padding="1rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="10px",
                    width="100%",
                ),
                spacing="6",
                align_items="start",
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading("Scenario Navigator", size="6", color=TEXT_PRIMARY, weight="bold"),
                    rx.text(
                        "Pick a scenario and jump to the full step-by-step guide below.",
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
                    _scenario_jump_card(
                        title="Store Data On Chain",
                        description="Start with the smallest useful contract: seed state, save a value, read it back.",
                        target="scenario-store-data",
                        icon="database",
                    ),
                    _scenario_jump_card(
                        title="Token From Scratch",
                        description="Build an XSC0001-style token and see how each required function maps to behavior.",
                        target="scenario-token-from-scratch",
                        icon="list_checks",
                    ),
                    _scenario_jump_card(
                        title="Multisig Treasury",
                        description="Require multiple owner approvals before contract funds are moved.",
                        target="scenario-multisig",
                        icon="shield",
                    ),
                    _scenario_jump_card(
                        title="Upgradable Router",
                        description="Route calls to an implementation contract and switch targets without changing entrypoint.",
                        target="scenario-upgradable-contracts",
                        icon="layers",
                    ),
                    columns={"base": "1", "md": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading(
                        "Scenario 1: Store Data On Chain",
                        anchor_id="scenario-store-data",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "This is the smallest complete storage contract pattern: one write method and one read method.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    _tutorial_step(
                        1,
                        "Declare persistent state",
                        why="Contract state must be declared at module scope so values persist between transactions and remain queryable by clients.",
                        how="Use a `Hash` for key-value records so each key can be addressed independently and updated without rewriting unrelated state.",
                        snippet=STORE_DATA_STEP_1,
                    ),
                    _tutorial_step(
                        2,
                        "Implement the write path",
                        why="Validate all on-chain mutations before writes: writes consume chi, and Contracting has no `try/except` recovery.",
                        how="Create a `save(key, value)` export, guard invalid input with `assert`, then write to `records[key]` in one explicit mutation path.",
                        snippet=STORE_DATA_STEP_2,
                    ),
                    _tutorial_step(
                        3,
                        "Implement the read path",
                        why="Read functions are the stable external API for wallets, indexers, and apps that need deterministic state access.",
                        how="Create `read(key)` that returns `records[key]`; with `default_value=''`, missing keys return an empty string instead of failing.",
                        snippet=STORE_DATA_STEP_3,
                    ),
                    spacing="4",
                    align_items="start",
                    width="100%",
                ),
                subsection(
                    "Full Contract",
                    copyable_code_block(
                        STORE_DATA_FULL,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="store-data-full-contract",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    rx.flex(
                        linked_heading(
                            "Scenario 2: Write a Token From Scratch",
                            anchor_id="scenario-token-from-scratch",
                            size="6",
                            color=TEXT_PRIMARY,
                            weight="bold",
                        ),
                        section_action_links(
                            [
                                {
                                    "label": "XSC0001",
                                    "icon": "book_open",
                                    "href": "https://docs.xian.org/contracts/standards/xsc0001",
                                }
                            ],
                        ),
                        direction={"base": "column", "md": "row"},
                        align_items={"base": "start", "md": "center"},
                        justify="between",
                        gap="0.75rem",
                        width="100%",
                    ),
                    rx.text(
                        "This walkthrough derives a minimal token from XSC0001 interface expectations so each method has a clear reason to exist.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    _tutorial_step(
                        1,
                        "Define required storage",
                        why="Tokens need balances, delegated spending records, and metadata so wallets show holdings and integrations route calls predictably.",
                        how="Use `balances`, `approvals`, and `metadata` hashes as the base model; this maps to transfer, allowance, and token-info read paths.",
                        snippet=TOKEN_STEP_1,
                    ),
                    _tutorial_step(
                        2,
                        "Seed metadata and initial supply",
                        why="Set canonical defaults at deployment so downstream tools get a stable symbol/name and governance authority from block one.",
                        how="In `seed`, set metadata fields, assign `operator`, and mint initial supply to the deployer address for deterministic initial ownership.",
                        snippet=TOKEN_STEP_2,
                    ),
                    _tutorial_step(
                        3,
                        "Implement holder balance and direct transfer",
                        why="`balance_of` and `transfer` are the core wallet actions, so they must be minimal, explicit, and easy to reason about.",
                        how="Return balances by account and move funds by debiting caller then crediting recipient with positive-amount and sufficient-balance guards.",
                        snippet=TOKEN_STEP_3,
                    ),
                    _tutorial_step(
                        4,
                        "Add delegated transfer behavior",
                        why="DEXes and routers often execute on behalf of users, so allowance-based delegation is required for composability.",
                        how="Use `approve` to set spender allowance and `transfer_from` to validate and consume it before moving owner funds.",
                        snippet=TOKEN_STEP_4,
                    ),
                    _tutorial_step(
                        5,
                        "Gate metadata updates by operator",
                        why="Metadata is user-facing and should not be mutable by arbitrary callers, otherwise explorers and wallets can be spoofed or degraded.",
                        how="Add `change_metadata` with an `operator` check so only governance authority can update mutable token fields.",
                        snippet=TOKEN_STEP_5,
                    ),
                    spacing="4",
                    align_items="start",
                    width="100%",
                ),
                subsection(
                    "Full Contract",
                    copyable_code_block(
                        TOKEN_FULL,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="token-from-scratch-full-contract",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading(
                        "Scenario 3: Multisig Contract",
                        anchor_id="scenario-multisig",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "This pattern protects treasury actions by requiring multiple owner approvals before execution.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    _tutorial_step(
                        1,
                        "Create owner + proposal state",
                        why="Multisig requires explicit ownership, per-proposal approval tracking, and deterministic counters to prevent ambiguous execution state.",
                        how="Use owner flags plus proposal/approval hashes and counters so each proposal has an auditable lifecycle from creation to execution.",
                        snippet=MULTISIG_STEP_1,
                    ),
                    _tutorial_step(
                        2,
                        "Initialize owner set and threshold",
                        why="The approval threshold is the core safety boundary, so it must be fixed at deployment and validated immediately.",
                        how="In `seed`, register each owner, assert a sane threshold, and initialize proposal counters so IDs are deterministic.",
                        snippet=MULTISIG_STEP_2,
                    ),
                    _tutorial_step(
                        3,
                        "Propose a transfer",
                        why="Splitting proposal from execution creates a review window so funds cannot move in a single unilateral action.",
                        how="Store transfer intent in `proposals` and auto-approve by proposer to reduce one extra approval transaction.",
                        snippet=MULTISIG_STEP_3,
                    ),
                    _tutorial_step(
                        4,
                        "Collect approvals",
                        why="Each owner should approve at most once; duplicate approvals must be blocked to preserve threshold integrity.",
                        how="Track approval flags by `(proposal_id, owner)` and trigger execution exactly when approval count reaches `required_approvals`.",
                        snippet=MULTISIG_STEP_4,
                    ),
                    _tutorial_step(
                        5,
                        "Execute by calling token contract",
                        why="Once governance conditions pass, treasury movement should happen in one internal execution step that records completion.",
                        how="Import contract via `importlib.import_module` and call `transfer`.",
                        snippet=MULTISIG_STEP_5,
                    ),
                    spacing="4",
                    align_items="start",
                    width="100%",
                ),
                rx.box(
                    text_with_inline_code(
                        "Operational note: this contract must hold token balance first (for example by direct transfer to `ctx.this`) "
                        "before proposals can execute outgoing transfers.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.6",
                        width="100%",
                    ),
                    padding="1rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="10px",
                    width="100%",
                ),
                subsection(
                    "Full Contract",
                    copyable_code_block(
                        MULTISIG_FULL,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="multisig-full-contract",
                ),
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading(
                        "Scenario 4: Upgradable Contracts",
                        anchor_id="scenario-upgradable-contracts",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "Use a router contract as stable entrypoint, forward calls to an implementation contract, and switch the target later.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="3",
                    align_items="start",
                    width="100%",
                ),
                rx.vstack(
                    _tutorial_step(
                        1,
                        "Write implementation v1",
                        why="Router upgrades are safest when implementations share a stable function interface from day one.",
                        how="Start with a simple counter contract exposing `increment` and `current`; this becomes the interface contract callers depend on.",
                        snippet=UPGRADE_V1,
                    ),
                    _tutorial_step(
                        2,
                        "Write implementation v2 with same interface",
                        why="Keeping signatures identical allows upgrades without breaking client code that already integrates with the router.",
                        how="Keep function names/arguments exactly the same while changing internal behavior in v2.",
                        snippet=UPGRADE_V2,
                    ),
                    _tutorial_step(
                        3,
                        "Declare router state",
                        why="The router needs explicit authority and one canonical pointer to decide which implementation handles calls.",
                        how="Store `admin` and `active_contract` in `Variable`s so upgrades are controlled and queryable on-chain.",
                        snippet=UPGRADE_ROUTER_STEP_1 + "\n\n" + UPGRADE_ROUTER_STEP_2,
                    ),
                    _tutorial_step(
                        4,
                        "Forward calls from router to implementation",
                        why="Forwarding preserves one stable entrypoint address while allowing implementation logic to evolve over time.",
                        how="Load the selected implementation with `importlib.import_module`, then call the same exported method signatures on that target.",
                        snippet=UPGRADE_ROUTER_STEP_3,
                    ),
                    _tutorial_step(
                        5,
                        "Add controlled upgrade switch",
                        why="Upgrade authority must be explicit; otherwise any caller could redirect execution to malicious contracts.",
                        how="Protect `set_active_contract` with an admin check and expose `get_active_contract` so UIs and bots can verify active implementation.",
                        snippet=UPGRADE_ROUTER_STEP_4 + "\n\n" + UPGRADE_ROUTER_STEP_5,
                    ),
                    spacing="4",
                    align_items="start",
                    width="100%",
                ),
                rx.box(
                    rx.text(
                        "Design note: this router pattern upgrades behavior. If each implementation keeps its own state, state may differ per implementation. "
                        "For production upgrades with shared state, keep storage in a dedicated contract or proxy storage layer.",
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
                subsection(
                    "Router Contract",
                    copyable_code_block(
                        UPGRADE_ROUTER_FULL,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="upgradable-router-contract",
                ),
                subsection(
                    "Upgrade Call Flow",
                    copyable_code_block(
                        UPGRADE_CALL_FLOW,
                        language="python",
                        show_line_numbers=False,
                        wrap_long_lines=False,
                    ),
                    id="upgradable-call-flow",
                ),
                subsection(
                    "Implementation v1",
                    copyable_code_block(
                        UPGRADE_V1,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="upgradable-implementation-v1",
                ),
                subsection(
                    "Implementation v2",
                    copyable_code_block(
                        UPGRADE_V2,
                        language="python",
                        show_line_numbers=True,
                        wrap_long_lines=False,
                    ),
                    id="upgradable-implementation-v2",
                ),
            )
        ),
    )


__all__ = ["tutorials_page"]
