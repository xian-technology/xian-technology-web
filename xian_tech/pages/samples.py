import reflex as rx

from ..components.common import (
    copyable_code_block,
    hover_icon_chip,
    icon_watermark_hover_card,
    linked_heading,
    page_layout,
    section,
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
from ..state import SamplesState

SEARCH_SECTIONS = [
    {
        "id": "samples-page",
        "title": "Samples & Scenarios",
        "subtitle": "Production-style examples for xian-py and BDS workflows.",
        "category": "Developers",
        "badge": "Page",
        "href": "/samples",
        "keywords": ["Samples", "Scenarios", "xian-py", "BDS", "GraphQL"],
    },
    {
        "id": "samples-scenario-transfer-confirmation",
        "title": "Scenario: Reliable Transfer Confirmation",
        "subtitle": "Send a transfer, wait for finalization, and fail fast on terminal errors.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/samples#scenario-transfer-confirmation",
        "keywords": ["xian-py", "send", "transaction", "wait", "polling", "confirmation", "websocket"],
    },
    {
        "id": "samples-scenario-contract-call-guardrails",
        "title": "Scenario: Simulate, Estimate, Submit",
        "subtitle": "Preview state deltas, validate expected output, then submit with simulated chi.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/samples#scenario-contract-call-guardrails",
        "keywords": ["simulate", "send_tx", "state", "chi", "dex", "slippage"],
    },
    {
        "id": "samples-scenario-bds-retrieval",
        "title": "Scenario: BDS Retrieval and Pagination",
        "subtitle": "Query transfer history and state snapshots through GraphQL.",
        "category": "Developers",
        "badge": "Scenario",
        "href": "/samples#scenario-bds-retrieval",
        "keywords": ["BDS", "GraphQL", "pagination", "events", "state"],
    },
]

SCENARIO_TRANSFER_SYNC = '''from time import monotonic, sleep
from xian_py import Wallet, Xian

# Node RPC endpoint.
NODE_URL = "http://node-ip:26657"


def wait_for_tx(xian: Xian, tx_hash: str, timeout_seconds: int = 45) -> dict:
    """Poll tx status until success, failure, or timeout."""
    deadline = monotonic() + timeout_seconds

    while monotonic() < deadline:
        # Check latest tx status from the node.
        tx = xian.get_tx(tx_hash)

        if tx.get("success") is True:
            return tx

        # "Not found" usually means tx is still propagating/indexing.
        message = str(tx.get("message", "")).lower()
        if "not found" in message:
            sleep(2)
            continue

        # Any other response is treated as terminal failure.
        raise RuntimeError(f"Transaction failed: {tx}")

    raise TimeoutError(f"Timed out waiting for tx {tx_hash}")


def send_and_confirm(recipient: str, amount: float) -> dict:
    # Build wallet + sync client for this workflow.
    wallet = Wallet()
    xian = Xian(NODE_URL, wallet=wallet)

    # Submit transfer transaction.
    submit = xian.send(amount=amount, to_address=recipient)
    if not submit.get("success"):
        raise RuntimeError(submit.get("message", "submit failed"))

    # If no hash is returned, forward submit response as-is.
    tx_hash = submit.get("tx_hash")
    if not tx_hash:
        return submit

    # Otherwise wait for final tx resolution.
    return wait_for_tx(xian, tx_hash)


# Example usage.
result = send_and_confirm("recipient_address", 5)
print(result)'''

SCENARIO_TRANSFER_ASYNC = '''import asyncio
from xian_py import Wallet, XianAsync

# Node RPC endpoint.
NODE_URL = "http://node-ip:26657"


async def wait_for_tx(client: XianAsync, tx_hash: str, timeout_seconds: int = 45) -> dict:
    # Use loop time to avoid wall-clock drift issues.
    deadline = asyncio.get_running_loop().time() + timeout_seconds

    while asyncio.get_running_loop().time() < deadline:
        # Fetch the latest transaction state.
        tx = await client.get_tx(tx_hash)

        if tx.get("success") is True:
            return tx

        # Keep polling while tx is still not indexed.
        message = str(tx.get("message", "")).lower()
        if "not found" in message:
            await asyncio.sleep(2)
            continue

        # Stop immediately on terminal failure.
        raise RuntimeError(f"Transaction failed: {tx}")

    raise TimeoutError(f"Timed out waiting for tx {tx_hash}")


async def transfer_with_confirmation(recipient: str, amount: float) -> dict:
    wallet = Wallet()

    # Reuse a single async client session for submit + polling.
    async with XianAsync(NODE_URL, wallet=wallet) as client:
        # Broadcast transfer.
        submit = await client.send(amount=amount, to_address=recipient)
        if not submit.get("success"):
            raise RuntimeError(submit.get("message", "submit failed"))

        # Return immediate response if hash is unavailable.
        tx_hash = submit.get("tx_hash")
        if not tx_hash:
            return submit

        # Otherwise wait for a final success/fail result.
        return await wait_for_tx(client, tx_hash)


# Example usage.
print(asyncio.run(transfer_with_confirmation("recipient_address", 5)))'''

SCENARIO_TRANSFER_WS_TRACKING = '''import asyncio
import json
import websockets

from xian_py import Wallet, XianAsync
from xian_py.encoding import decode_str

# HTTP and websocket endpoints for the same node.
NODE_HTTP = "http://node-ip:26657"
NODE_WS = NODE_HTTP.replace("http://", "ws://").replace("https://", "wss://") + "/websocket"


def _hashes_from_event(events: dict) -> list[str]:
    # Normalize tx hash values to a consistent list format.
    raw_hashes = events.get("tx.hash", [])
    hashes = raw_hashes if isinstance(raw_hashes, list) else [raw_hashes]
    return [item.upper() for item in hashes if item]


async def wait_for_tx_event(tx_hash: str, timeout_seconds: int = 45) -> tuple[bool, str]:
    tx_hash = tx_hash.upper()

    # Subscribe to chain tx events over websocket.
    async with websockets.connect(NODE_WS, ping_interval=20, ping_timeout=30) as ws:
        await ws.send(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "subscribe",
                    "id": 1,
                    "params": {"query": "tm.event='Tx'"},
                }
            )
        )

        while True:
            # Wait for the next event frame and decode payload.
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout_seconds)
            message = json.loads(raw)
            result = message.get("result", {})
            events = result.get("events", {})

            # Ignore events from other transactions.
            if tx_hash not in _hashes_from_event(events):
                continue

            # Parse tx execution result.
            tx_result = result.get("data", {}).get("value", {}).get("TxResult", {}).get("result", {})
            encoded = tx_result.get("data")

            # Some responses only expose code/log.
            if not encoded:
                success = tx_result.get("code", 1) == 0
                return (success, tx_result.get("log", "no tx detail"))

            # Decode structured tx result payload.
            decoded = json.loads(decode_str(encoded))
            success = decoded.get("status") == 0
            detail = decoded.get("result", "")
            return (success, detail if detail != "None" else "")


async def send_and_confirm_ws(recipient: str, amount: float) -> tuple[bool, str]:
    wallet = Wallet()

    # Submit via HTTP RPC and confirm via websocket events.
    async with XianAsync(NODE_HTTP, wallet=wallet) as client:
        submit = await client.send(amount=amount, to_address=recipient)
        if not submit.get("success"):
            raise RuntimeError(submit.get("message", "submit failed"))

        # If no hash is available, treat submission as accepted.
        tx_hash = submit.get("tx_hash")
        if not tx_hash:
            return (True, "submitted without tx hash")

        # Block until we receive this tx event.
        return await wait_for_tx_event(tx_hash)


# Example usage.
print(asyncio.run(send_and_confirm_ws("recipient_address", 5)))'''

SCENARIO_CONTRACT_GUARDRAILS = '''from xian_py import Wallet, Xian

NODE_URL = "http://node-ip:26657"

# Wallet + client setup.
wallet = Wallet()
xian = Xian(NODE_URL, wallet=wallet)

# Swap simulation target + acceptance threshold.
DEX_CONTRACT = "con_dex"
BUY_FUNCTION = "buy"
TOKEN_OUT = "con_token_b"
EXPECTED_MIN_OUT = 24.5

kwargs = {
    "token_in": "con_token_a",
    "token_out": TOKEN_OUT,
    "amount_in": 10,
    "min_amount_out": EXPECTED_MIN_OUT,
}


def _state_value(changes: list[dict], key: str):
    # Extract a single key from simulation state diff.
    for change in changes:
        if change.get("key") == key:
            return change.get("value")
    return None


# 1) Simulate the exact tx to get projected state changes and chi usage.
simulation = xian.simulate(DEX_CONTRACT, BUY_FUNCTION, kwargs)
if simulation.get("status") != 0:
    raise RuntimeError(f"Simulation failed: {simulation}")

# 2) Read predicted token-out amount from simulated state changes.
out_key = f"{TOKEN_OUT}.balances:{wallet.public_key}"
before_out = float(xian.get_state(TOKEN_OUT, "balances", wallet.public_key) or 0)
after_out = _state_value(simulation.get("state", []), out_key)
if after_out is None:
    raise RuntimeError(f"Simulation did not include expected key: {out_key}")

simulated_tokens_out = float(after_out) - before_out
if simulated_tokens_out < EXPECTED_MIN_OUT:
    raise RuntimeError(
        f"Expected at least {EXPECTED_MIN_OUT}, simulation returned {simulated_tokens_out}"
    )

# 3) Use simulated chi usage as the tx chi budget for the real call.
chi = int(simulation["chi_used"])
submit = xian.send_tx(
    DEX_CONTRACT,
    BUY_FUNCTION,
    kwargs,
    chi=chi,
    mode="commit",
)
if submit.receipt is None or not submit.receipt.success:
    raise RuntimeError(submit.receipt.message if submit.receipt else "submit failed")

print(
    {
        "simulated_tokens_out": simulated_tokens_out,
        "chi": chi,
        "tx_hash": submit.tx_hash,
    }
)'''

SCENARIO_BDS_RETRIEVAL = '''import requests
from typing import Any

# GraphQL endpoint exposed by BDS.
BDS_GRAPHQL_URL = "http://node-ip:26657/graphql"

# Query transfer events to a target address with cursor pagination.
TRANSFER_EVENTS_QUERY = """
query TransfersForAddress($to: String!, $after: Cursor) {
  allEvents(
    first: 200
    after: $after
    condition: {event: "Transfer"}
    filter: {dataIndexed: {contains: {to: $to}}}
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    edges {
      node {
        id
        txHash
        blockNum
        dataIndexed
        data
      }
    }
  }
}
"""

# Query one state key snapshot (e.g., current balance).
BALANCE_QUERY = """
query BalanceByKey($key: String!) {
  allStates(condition: {key: $key}) {
    edges {
      node {
        key
        value
      }
    }
  }
}
"""


def run_query(query: str, variables: dict[str, Any]) -> dict[str, Any]:
    # Execute one GraphQL request.
    response = requests.post(
        BDS_GRAPHQL_URL,
        json={"query": query, "variables": variables},
        timeout=20,
    )
    response.raise_for_status()

    # Surface GraphQL-layer errors explicitly.
    payload = response.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])

    return payload["data"]


def fetch_transfers(address: str) -> list[dict[str, Any]]:
    # Walk all pages and flatten event nodes.
    cursor = None
    rows: list[dict[str, Any]] = []

    while True:
        data = run_query(TRANSFER_EVENTS_QUERY, {"to": address, "after": cursor})
        block = data["allEvents"]
        rows.extend(edge["node"] for edge in block["edges"])

        if not block["pageInfo"]["hasNextPage"]:
            break

        cursor = block["pageInfo"]["endCursor"]

    return rows


def fetch_balance(address: str) -> str | None:
    # Read current balance value from state table projection.
    key = f"currency.balances:{address}"
    data = run_query(BALANCE_QUERY, {"key": key})
    edges = data["allStates"]["edges"]
    return edges[0]["node"]["value"] if edges else None


# Example usage.
address = "some_address"
transfer_history = fetch_transfers(address)
latest_balance = fetch_balance(address)

print({"transfer_count": len(transfer_history), "balance": latest_balance})'''


def _bullet_item(text: str) -> rx.Component:
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


def _ordered_step_item(step: int, text: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(str(step), size="2", weight="bold", color=ACCENT),
            min_width="1.4rem",
            height="1.4rem",
            display="inline-flex",
            align_items="center",
            justify_content="center",
            border=f"1px solid {ACCENT_GLOW}",
            background=ACCENT_SOFT,
            border_radius="999px",
        ),
        text_with_inline_code(
            text,
            size="3",
            color=TEXT_MUTED,
            line_height="1.6",
        ),
        spacing="2",
        align_items="center",
    )


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


def _code_example(code: str, *, copy_id: str, language: str = "python", tabbed: bool = False) -> rx.Component:
    return copyable_code_block(
        code,
        copied=SamplesState.code_copied_id == copy_id,
        on_copy=SamplesState.copy_code(code, copy_id),
        language=language,
        show_line_numbers=True,
        wrap_long_lines=False,
        block_margin_top="0.45rem" if tabbed else "0",
    )


def samples_page() -> rx.Component:
    """Production-ready examples and scenarios for Xian builders."""
    return page_layout(
        section(
            rx.vstack(
                rx.box(
                    rx.text("SAMPLES", size="2", letter_spacing="0.15em", color=ACCENT, weight="medium"),
                    padding="0.625rem 1.25rem",
                    background=ACCENT_SOFT,
                    border=f"1px solid {ACCENT_GLOW}",
                    border_radius="8px",
                ),
                rx.heading(
                    "Developer Scenarios",
                    size="8",
                    color=TEXT_PRIMARY,
                    weight="bold",
                    line_height="1.2",
                ),
                rx.text(
                    "Ready-made, end-to-end patterns for common blockchain tasks: submit transactions safely, verify final state, "
                    "and pull structured data from BDS with predictable query workflows.",
                    size="4",
                    color=TEXT_MUTED,
                    line_height="1.7",
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
                        "Pick a scenario and jump to the full walkthrough section below.",
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
                        title="Simulate, Estimate, Submit",
                        description="Preview simulated state deltas and only submit when expected output passes checks.",
                        target="scenario-contract-call-guardrails",
                        icon="code",
                    ),
                    _scenario_jump_card(
                        title="Reliable Transfer Confirmation",
                        description="Send token transfers with bounded polling and explicit success checks.",
                        target="scenario-transfer-confirmation",
                        icon="send",
                    ),
                    _scenario_jump_card(
                        title="BDS Retrieval and Pagination",
                        description="Use GraphQL to query events and state snapshots with production-safe pagination.",
                        target="scenario-bds-retrieval",
                        icon="database",
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
                    linked_heading(
                        "Scenario 1: Simulate, Estimate, Submit",
                        anchor_id="scenario-contract-call-guardrails",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "For state-changing calls like a DEX buy, simulate first, read the predicted state change, "
                        "and submit the real tx only when the simulated output matches your expectation.",
                        size="4",
                        color=TEXT_MUTED,
                        line_height="1.7",
                        width="100%",
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                rx.grid(
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("code", size=24),
                            rx.text("Flow", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _ordered_step_item(1, "Simulate the exact tx payload."),
                            _ordered_step_item(2, "Read the predicted token-out delta from simulated state."),
                            _ordered_step_item(3, "Abort when simulated output is below expectation."),
                            _ordered_step_item(4, "Set `chi` from simulation `chi_used`."),
                            _ordered_step_item(5, "Submit the real `send_tx` call with that chi budget."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="code",
                        padding="1.75rem",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("shield", size=24),
                            rx.text("Guardrails", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _bullet_item("Treat non-zero simulation status as a hard stop."),
                            _bullet_item("Fail when expected state keys are missing in simulation output."),
                            _bullet_item("Enforce minimum output thresholds before broadcasting."),
                            _bullet_item("Use simulated chi to avoid underfunded tx attempts."),
                            _bullet_item("Handle unsuccessful submit responses as terminal failures."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="shield",
                        padding="1.75rem",
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Code",
                    _code_example(SCENARIO_CONTRACT_GUARDRAILS, copy_id="scenario-contract-guardrails"),
                    id="scenario-contract-call-guardrails-code",
                ),
                rx.box(
                    rx.text(
                        "Important: this simulation preview is not a guarantee of final execution state. "
                        "If another transaction front-runs and changes state before your tx executes, your real result can differ.",
                        size="3",
                        color=TEXT_MUTED,
                        line_height="1.6",
                    ),
                    rx.text(
                        "If you need strict guarantees, run the action from your own contract and assert the final conditions there. "
                        "When the result is outside your bounds, fail with an `assert` so the transaction reverts.",
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
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading(
                        "Scenario 2: Reliable Transfer Confirmation",
                        anchor_id="scenario-transfer-confirmation",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "This scenario covers a full transfer lifecycle: submit the transfer, poll for final tx status, "
                        "and stop cleanly on timeout or terminal failure.",
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
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("list_checks", size=24),
                            rx.text("Flow", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _ordered_step_item(1, "Create wallet + client once per workflow."),
                            _ordered_step_item(2, "Submit via `send` and require a successful response."),
                            _ordered_step_item(3, "If a hash exists, poll `get_tx` until success/fail/timeout."),
                            _ordered_step_item(4, "Retry only while status is unresolved, not on hard failures."),
                            _ordered_step_item(5, "Return one final object your app can log and persist."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="list_checks",
                        padding="1.75rem",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("gauge", size=24),
                            rx.text("What to verify", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _bullet_item("Submission returned `success=True`."),
                            _bullet_item("A tx hash is captured when available."),
                            _bullet_item("Polling stops within a bounded timeout window."),
                            _bullet_item("Final receipt reports success before user feedback."),
                            _bullet_item("Failures include actionable message + tx hash context."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="gauge",
                        padding="1.75rem",
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Code",
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Sync", value="sync", color_scheme="green"),
                            rx.tabs.trigger("Async", value="async", color_scheme="green"),
                            rx.tabs.trigger("Advanced WS", value="ws", color_scheme="green"),
                            gap="0.75rem",
                            wrap="wrap",
                        ),
                        rx.tabs.content(
                            _code_example(SCENARIO_TRANSFER_SYNC, copy_id="scenario-transfer-sync", tabbed=True),
                            value="sync",
                            width="100%",
                        ),
                        rx.tabs.content(
                            _code_example(SCENARIO_TRANSFER_ASYNC, copy_id="scenario-transfer-async", tabbed=True),
                            value="async",
                            width="100%",
                        ),
                        rx.tabs.content(
                            _code_example(SCENARIO_TRANSFER_WS_TRACKING, copy_id="scenario-transfer-ws", tabbed=True),
                            value="ws",
                            width="100%",
                        ),
                        default_value="sync",
                        width="100%",
                        min_width="0",
                    ),
                    id="scenario-transfer-confirmation-code",
                ),
                rx.box(
                    rx.text(
                        "Advanced WS note: this event-driven variant is better for long-running bots and high-throughput workers. "
                        "For production, add reconnect backoff and pending-tx resubscription, similar to xian-tg-bot.",
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
            )
        ),
        section(
            section_panel(
                rx.vstack(
                    linked_heading(
                        "Scenario 3: BDS Retrieval and Pagination",
                        anchor_id="scenario-bds-retrieval",
                        size="6",
                        color=TEXT_PRIMARY,
                        weight="bold",
                    ),
                    rx.text(
                        "This scenario shows how to read transfer history and state snapshots from BDS GraphQL, with cursor pagination "
                        "and structured error handling for production services.",
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
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("database", size=24),
                            rx.text("Flow", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _ordered_step_item(1, "Define event and state queries as separate operations."),
                            _ordered_step_item(2, "Wrap POST execution in a single `run_query` helper."),
                            _ordered_step_item(3, "Iterate with `endCursor` until `hasNextPage=False`."),
                            _ordered_step_item(4, "Store normalized rows, not raw GraphQL envelopes."),
                            _ordered_step_item(5, "Merge event history with latest balance snapshots."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="database",
                        padding="1.75rem",
                    ),
                    icon_watermark_hover_card(
                        rx.hstack(
                            hover_icon_chip("layers", size=24),
                            rx.text("Data handling", size="3", weight="bold", color=TEXT_PRIMARY),
                            spacing="3",
                            align_items="center",
                        ),
                        rx.vstack(
                            _bullet_item("Check `errors` in every GraphQL response payload."),
                            _bullet_item("Capture count + cursor for resumable polling jobs."),
                            _bullet_item("Preserve tx hash and block number for audit trails."),
                            _bullet_item("Treat empty `edges` as valid empty-result state."),
                            _bullet_item("Use schema-aligned fields to reduce parser breakage."),
                            spacing="2",
                            align_items="start",
                        ),
                        icon="layers",
                        padding="1.75rem",
                    ),
                    columns={"base": "1", "lg": "2"},
                    spacing="4",
                    width="100%",
                    align="stretch",
                ),
                subsection(
                    "Code",
                    _code_example(SCENARIO_BDS_RETRIEVAL, copy_id="scenario-bds-retrieval"),
                    id="scenario-bds-retrieval-code",
                ),
            )
        ),
    )


__all__ = ["samples_page"]
