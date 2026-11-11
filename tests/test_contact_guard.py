import pytest

from xian_tech import contact_guard
from xian_tech.contact_guard import (
    ContactRateLimiter,
    contact_client_key,
    contact_field_errors,
)


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def limiter(clock, **overrides):
    settings = dict(
        per_client_limit=2,
        per_client_window_seconds=60,
        global_limit=5,
        global_window_seconds=60,
        max_tracked_clients=100,
        clock=clock,
    )
    settings.update(overrides)
    return ContactRateLimiter(**settings)


def test_per_client_limit_blocks_until_tokens_refill():
    clock = Clock()
    guard = limiter(clock)
    assert guard.allow("1.1.1.1")
    assert guard.allow("1.1.1.1")
    assert not guard.allow("1.1.1.1")
    assert guard.allow("2.2.2.2"), "another client keeps its own budget"
    clock.now += 30  # half a window refills one token
    assert guard.allow("1.1.1.1")
    assert not guard.allow("1.1.1.1")


def test_global_limit_caps_total_submissions_across_clients():
    clock = Clock()
    guard = limiter(clock)
    allowed = [guard.allow(f"10.0.0.{index}") for index in range(8)]
    assert allowed == [True] * 5 + [False] * 3


def test_global_bucket_refills_at_limit_per_window():
    clock = Clock()
    guard = limiter(clock)
    for index in range(5):
        assert guard.allow(f"c{index}")
    clock.now += 12  # 5 per 60s refills one token every 12s
    assert guard.allow("x")
    assert not guard.allow("y")


def test_rejected_client_does_not_spend_global_budget():
    clock = Clock()
    guard = limiter(clock, global_limit=3)
    assert guard.allow("a") and guard.allow("a")
    for _ in range(10):
        assert not guard.allow("a")
    assert guard.allow("b"), "a blocked client must not drain the global bucket"


def test_global_rejection_does_not_spend_client_budget():
    clock = Clock()
    guard = limiter(clock, global_limit=2, per_client_window_seconds=6000)
    assert guard.allow("a") and guard.allow("a")
    assert not guard.allow("b"), "global budget exhausted"
    clock.now += 60  # global bucket refills; client buckets barely move
    assert guard.allow("b") and guard.allow("b"), "b keeps both of its tokens"


def test_tracked_clients_are_bounded():
    clock = Clock()
    guard = limiter(clock, global_limit=10_000, max_tracked_clients=3)
    for index in range(50):
        guard.allow(f"client-{index}")
    assert guard.tracked_clients() == 3


def test_eviction_drops_the_least_recently_seen_client():
    clock = Clock()
    guard = limiter(clock, global_limit=10_000, max_tracked_clients=2)
    assert guard.allow("a") and guard.allow("a")
    guard.allow("b")
    assert not guard.allow("a")  # a is now the most recently seen
    guard.allow("c")  # evicts b, not the exhausted a
    assert not guard.allow("a")
    assert guard.allow("b") and guard.allow("b"), "evicted b restarts with a full bucket"


@pytest.mark.parametrize(
    ("raw", "expected"), [("", 7.0), ("5", 5.0), ("1", 1.0), ("0", 7.0), ("-1", 7.0), ("abc", 7.0)]
)
def test_env_numbers_fall_back_on_missing_or_invalid_values(monkeypatch, raw, expected):
    monkeypatch.setenv("CONTACT_TEST_NUMBER", raw)
    assert contact_guard._env_number("CONTACT_TEST_NUMBER", 7) == expected


@pytest.mark.parametrize(("raw", "expected"), [("", 0), ("2", 2), ("x", 0), ("-1", 0)])
def test_trusted_proxy_hops_from_env(monkeypatch, raw, expected):
    monkeypatch.setenv("CONTACT_TRUSTED_PROXY_HOPS", raw)
    assert contact_guard.trusted_proxy_hops_from_env() == expected


def test_client_key_uses_socket_peer_and_ignores_spoofable_forwarded_for():
    headers = {"asgi-scope-client": "203.0.113.9", "x-forwarded-for": "1.2.3.4"}
    assert contact_client_key(headers, trusted_proxy_hops=0) == "203.0.113.9"


def test_client_key_takes_the_address_appended_by_trusted_proxies():
    headers = {
        "asgi-scope-client": "10.0.0.2",
        "x-forwarded-for": "6.6.6.6, 198.51.100.7",
    }
    # One trusted proxy appended the real client as the right-most entry;
    # anything left of it is client-controlled.
    assert contact_client_key(headers, trusted_proxy_hops=1) == "198.51.100.7"
    assert contact_client_key(headers, trusted_proxy_hops=2) == "6.6.6.6"
    assert contact_client_key(headers, trusted_proxy_hops=3) == "10.0.0.2"
    assert contact_client_key({}, trusted_proxy_hops=0) == "unknown"


@pytest.mark.parametrize(
    ("field", "limit"),
    [
        ("name", contact_guard.MAX_NAME_LENGTH),
        ("organization", contact_guard.MAX_ORGANIZATION_LENGTH),
        ("topic", contact_guard.MAX_TOPIC_LENGTH),
        ("message", contact_guard.MAX_MESSAGE_LENGTH),
    ],
)
def test_field_length_caps(field, limit):
    fields = {"name": "", "organization": "", "topic": "", "message": "hello"}
    fields[field] = "x" * limit
    assert contact_field_errors(**fields) == {}
    fields[field] = "x" * (limit + 1)
    assert set(contact_field_errors(**fields)) == {field}


def test_validation_and_mail_composition():
    from xian_tech.contact_email import compose_contact_email
    from xian_tech.contact_guard import ContactSubmission, validate_contact_submission

    ok = ContactSubmission("Ada", "ada@example.com", "", "Grants", "Hello")
    assert validate_contact_submission(ok).form_error == ""
    assert compose_contact_email(ok) == (
        "Grants - Ada",
        "Name: Ada\nEmail: ada@example.com\nTopic: Grants\n\nHello",
    )
    anonymous = ContactSubmission("", "ada@example.com", "DAO", "", "Hi")
    assert compose_contact_email(anonymous)[0] == "Foundation contact - ada@example.com"
    bad = validate_contact_submission(ContactSubmission("", "nope", "", "", ""))
    assert bad.email_error and bad.message_error
    assert bad.form_error == "Please fix the highlighted fields below."
