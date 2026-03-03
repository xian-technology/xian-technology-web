from __future__ import annotations
from email.message import EmailMessage
from email.utils import make_msgid

import os
import smtplib
import ssl


def _coerce_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _sanitize_header(value: str) -> str:
    return value.replace("\n", " ").replace("\r", " ").strip()


def send_contact_email(
    subject: str,
    body: str,
    *,
    sender: str,
    recipient: str,
    reply_to: str | None = None,
) -> None:
    host = os.getenv("SMTP_HOST", "").strip()
    if not host:
        raise ValueError("SMTP_HOST is not configured.")

    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME", "").strip()
    password = os.getenv("SMTP_PASSWORD", "").strip()
    use_tls = _coerce_bool(os.getenv("SMTP_USE_TLS"), default=True)
    use_ssl = _coerce_bool(os.getenv("SMTP_USE_SSL"), default=False)

    if username and not password:
        raise ValueError("SMTP_PASSWORD is required when SMTP_USERNAME is set.")

    message = EmailMessage()
    message["Message-ID"] = make_msgid(domain=host)
    message["Subject"] = _sanitize_header(subject)
    message["From"] = _sanitize_header(sender)
    message["To"] = _sanitize_header(recipient)
    if reply_to:
        message["Reply-To"] = _sanitize_header(reply_to)
    message.set_content(body)

    context = ssl.create_default_context()
    if use_ssl:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            if username:
                server.login(username, password)
            server.send_message(message)
        return

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        if use_tls:
            server.starttls(context=context)
            server.ehlo()
        if username:
            server.login(username, password)
        server.send_message(message)
