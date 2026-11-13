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


def test_live_email_validation_reports_missing_and_malformed_addresses():
    state = make_state()
    state.contact_status = "Sent"
    state.contact_error = "old error"

    state.set_contact_email("   ")
    assert state.contact_email_error == contact_guard.MISSING_EMAIL_MESSAGE
    assert (state.contact_status, state.contact_error) == ("", "")

    state.set_contact_email("not-an-email")
    assert state.contact_email_error == contact_guard.INVALID_EMAIL_MESSAGE

    state.set_contact_email(" ada@example.com ")
    assert state.contact_email_error == ""
    assert state.contact_form_email == " ada@example.com "


def test_live_message_validation_requires_text():
    state = make_state()
    state.contact_error = "old error"

    state.set_contact_message("  \n ")
    assert state.contact_message_error == contact_guard.MISSING_MESSAGE_MESSAGE
    assert state.contact_error == ""

    state.set_contact_message("Hello")
    assert state.contact_message_error == ""
    assert state.contact_form_message == "Hello"


def test_live_message_validation_applies_the_length_cap():
    state = make_state()
    limit = contact_guard.MAX_MESSAGE_LENGTH

    state.set_contact_message(" " + "x" * limit + " ")
    assert state.contact_message_error == ""

    state.set_contact_message("x" * (limit + 1))
    assert state.contact_message_error == "Keep this under 5,000 characters."


def test_typing_and_submitting_report_the_same_field_errors(monkeypatch):
    monkeypatch.setattr(app_state, "send_contact_email", lambda *a, **k: None)
    oversized = "x" * (contact_guard.MAX_MESSAGE_LENGTH + 1)
    for email, message in [("  ", oversized), ("not-an-email", "  ")]:
        typed = make_state()
        typed.set_contact_email(email)
        typed.set_contact_message(message)
        submitted = make_state("198.51.100.9")
        submit(submitted, {**FORM, "email": email, "message": message})
        assert submitted.contact_error == "Please fix the highlighted fields below."
        assert (submitted.contact_email_error, submitted.contact_message_error) == (
            typed.contact_email_error,
            typed.contact_message_error,
        )


def test_submission_is_ignored_while_one_is_in_flight_or_cooling_down(monkeypatch):
    sent = []
    monkeypatch.setattr(app_state, "send_contact_email", lambda *a, **k: sent.append(a))

    busy = make_state("198.51.100.3")
    busy.contact_submission_inflight = True
    busy.contact_error = "unchanged"
    submit(busy, FORM)
    assert busy.contact_error == "unchanged"

    cooling = make_state("198.51.100.4")
    cooling.contact_cooldown_remaining = 12
    submit(cooling, FORM)
    assert cooling.contact_error == "Please wait 12 seconds before sending another message."
    assert cooling.contact_submission_inflight is False
    assert sent == []
