"""Server-side abuse limits for the contact form.

Reflex keeps ``State`` per websocket session, so anything stored there can be
reset by opening a new session. The limiter here lives in the backend process
and is shared by every session: a per-client token bucket plus one global
bucket that bounds total mail volume even when client keys are spoofed or
shared behind a proxy.
"""

from __future__ import annotations

import os
import re
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Mapping

MAX_NAME_LENGTH = 200
MAX_ORGANIZATION_LENGTH = 200
MAX_TOPIC_LENGTH = 200
MAX_MESSAGE_LENGTH = 5000

_FIELD_LIMITS = {
    "name": MAX_NAME_LENGTH,
    "organization": MAX_ORGANIZATION_LENGTH,
    "topic": MAX_TOPIC_LENGTH,
    "message": MAX_MESSAGE_LENGTH,
}


EMAIL_PATTERN = re.compile(
    r"^(?=.{3,254}$)(?=.{1,64}@)[A-Z0-9](?:[A-Z0-9._%+-]{0,62}[A-Z0-9])?@"
    r"(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}$",
    re.IGNORECASE,
)
MISSING_EMAIL_MESSAGE = "Email is required."
INVALID_EMAIL_MESSAGE = "Enter a valid email address (example: name@domain.com)."
MISSING_MESSAGE_MESSAGE = "Please include a message so we can help."


@dataclass(frozen=True, slots=True)
class ContactSubmission:
    name: str
    email: str
    organization: str
    topic: str
    message: str


@dataclass(frozen=True, slots=True)
class ContactValidation:
    email_error: str = ""
    message_error: str = ""
    form_error: str = ""


def validate_contact_submission(submission: ContactSubmission) -> ContactValidation:
    """Check required fields, the email shape and length caps."""
    email_error = contact_email_error(submission.email)
    message_error = contact_message_error(submission.message)
    length_errors = contact_field_errors(
        name=submission.name,
        organization=submission.organization,
        topic=submission.topic,
        message=submission.message,
    )
    length_errors.pop("message", None)
    if length_errors:
        form_error = f"Please shorten these fields: {', '.join(sorted(length_errors))}."
    elif email_error or message_error:
        form_error = "Please fix the highlighted fields below."
    else:
        form_error = ""
    return ContactValidation(email_error, message_error, form_error)


def contact_email_error(email: str) -> str:
    """Explain what is wrong with a (stripped) email address, or return ""."""
    if not email:
        return MISSING_EMAIL_MESSAGE
    return "" if EMAIL_PATTERN.match(email) else INVALID_EMAIL_MESSAGE


def contact_message_error(message: str) -> str:
    """Explain what is wrong with a (stripped) message, or return ""."""
    if not message:
        return MISSING_MESSAGE_MESSAGE
    if len(message) > MAX_MESSAGE_LENGTH:
        return _too_long(MAX_MESSAGE_LENGTH)
    return ""


def _too_long(limit: int) -> str:
    return f"Keep this under {limit:,} characters."


def contact_field_errors(
    *, name: str, organization: str, topic: str, message: str
) -> dict[str, str]:
    """Return a message per field that exceeds its length cap."""
    values = {"name": name, "organization": organization, "topic": topic, "message": message}
    return {
        field: _too_long(limit)
        for field, limit in _FIELD_LIMITS.items()
        if len(values[field]) > limit
    }


def contact_client_key(headers: Mapping[str, str], trusted_proxy_hops: int) -> str:
    """Identify the submitting client without trusting client-written headers.

    With no trusted proxies the socket peer is used. With ``n`` trusted
    proxies in front of the app, the ``n``-th address from the right of
    ``X-Forwarded-For`` was appended by the outermost trusted proxy; entries
    further left are client-controlled and ignored.
    """
    peer = (headers.get("asgi-scope-client") or "").strip()
    if trusted_proxy_hops > 0:
        forwarded = [
            part.strip()
            for part in (headers.get("x-forwarded-for") or "").split(",")
            if part.strip()
        ]
        if len(forwarded) >= trusted_proxy_hops:
            return forwarded[-trusted_proxy_hops]
    return peer or "unknown"


@dataclass(slots=True)
class _Bucket:
    tokens: float
    updated: float

    def refill(self, now: float, capacity: float, rate: float) -> None:
        self.tokens = min(capacity, self.tokens + (now - self.updated) * rate)
        self.updated = now


class ContactRateLimiter:
    """Thread-safe per-client and global token buckets."""

    def __init__(
        self,
        *,
        per_client_limit: int,
        per_client_window_seconds: float,
        global_limit: int,
        global_window_seconds: float,
        max_tracked_clients: int = 10_000,
        clock: Callable[[], float] = time.monotonic,
    ):
        self._client_capacity = float(per_client_limit)
        self._client_rate = per_client_limit / per_client_window_seconds
        self._global_capacity = float(global_limit)
        self._global_rate = global_limit / global_window_seconds
        self._max_clients = max_tracked_clients
        self._clock = clock
        self._lock = threading.Lock()
        self._global = _Bucket(self._global_capacity, clock())
        self._clients: OrderedDict[str, _Bucket] = OrderedDict()

    def allow(self, client_key: str) -> bool:
        """Consume one submission for ``client_key`` when both budgets allow it."""
        with self._lock:
            now = self._clock()
            self._global.refill(now, self._global_capacity, self._global_rate)
            client = self._clients.pop(client_key, None) or _Bucket(self._client_capacity, now)
            client.refill(now, self._client_capacity, self._client_rate)
            self._clients[client_key] = client
            while len(self._clients) > self._max_clients:
                self._clients.popitem(last=False)
            if client.tokens < 1 or self._global.tokens < 1:
                return False
            client.tokens -= 1
            self._global.tokens -= 1
            return True

    def tracked_clients(self) -> int:
        with self._lock:
            return len(self._clients)


def _env_number(name: str, default: float) -> float:
    raw = os.getenv(name, "").strip()
    try:
        value = float(raw) if raw else default
    except ValueError:
        return default
    return value if value > 0 else default


def limiter_from_env() -> ContactRateLimiter:
    return ContactRateLimiter(
        per_client_limit=int(_env_number("CONTACT_RATE_PER_CLIENT", 3)),
        per_client_window_seconds=_env_number("CONTACT_RATE_PER_CLIENT_WINDOW_SECONDS", 600),
        global_limit=int(_env_number("CONTACT_RATE_GLOBAL", 30)),
        global_window_seconds=_env_number("CONTACT_RATE_GLOBAL_WINDOW_SECONDS", 3600),
    )


def trusted_proxy_hops_from_env() -> int:
    raw = os.getenv("CONTACT_TRUSTED_PROXY_HOPS", "").strip()
    return int(raw) if raw.isdigit() else 0
