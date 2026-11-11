import asyncio
import logging

from reflex.istate.data import RouterData

from xian_tech import contact_guard
from xian_tech.state import app as app_state
from xian_tech.state.app import State


def make_state(peer="203.0.113.5"):
    state = State(_reflex_internal_init=True)
    router_data = {"headers": {"asgi-scope-client": peer}, "pathname": "/contact"}
    object.__setattr__(state, "router_data", router_data)
    object.__setattr__(state, "router", RouterData.from_router_data(router_data))
    return state


def submit(state, form):
    async def drain():
        async for _ in state.submit_contact_form(form):
            pass

    asyncio.run(drain())


FORM = {"name": "Ada", "email": "ada@example.com", "topic": "Hi", "message": "Hello"}


def test_server_side_limit_survives_new_sessions(monkeypatch):
    sent = []
    monkeypatch.setattr(app_state, "send_contact_email", lambda *a, **k: sent.append(a))
    monkeypatch.setattr(
        app_state,
        "contact_limiter",
        contact_guard.ContactRateLimiter(
            per_client_limit=1,
            per_client_window_seconds=600,
            global_limit=100,
            global_window_seconds=600,
        ),
    )
    first = make_state()
    submit(first, FORM)
    assert first.contact_status and not first.contact_error
    second = make_state()  # a fresh websocket session from the same address
    submit(second, FORM)
    assert len(sent) == 1
    assert "too many" in second.contact_error.lower()


def test_oversized_message_is_rejected_without_sending(monkeypatch):
    sent = []
    monkeypatch.setattr(app_state, "send_contact_email", lambda *a, **k: sent.append(a))
    state = make_state("198.51.100.1")
    submit(state, {**FORM, "message": "x" * (contact_guard.MAX_MESSAGE_LENGTH + 1)})
    assert sent == []
    assert state.contact_message_error


def test_smtp_failure_is_logged_not_shown(monkeypatch, caplog):
    def fail(*args, **kwargs):
        raise RuntimeError("535 auth failed for smtp.internal.example user=relay")

    monkeypatch.setattr(app_state, "send_contact_email", fail)
    state = make_state("198.51.100.2")
    with caplog.at_level(logging.ERROR):
        submit(state, FORM)
    assert state.contact_error
    assert "smtp.internal.example" not in state.contact_error
    assert "535" not in state.contact_error
    assert "smtp.internal.example" in caplog.text
