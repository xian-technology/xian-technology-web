"""Lightweight Fizzy API helper (no client dependency)."""

from __future__ import annotations

import json
import re

from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin, urlsplit, urldefrag
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_PAGES = 100


def _origin(url: str) -> tuple[str, str, int]:
    parsed = urlsplit(url)
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("Fizzy URL must use an HTTP(S) origin without credentials")
    return (
        parsed.scheme,
        parsed.hostname.lower(),
        parsed.port if parsed.port is not None else (443 if parsed.scheme == "https" else 80),
    )


def _require_same_origin(base_url: str, url: str) -> str:
    if _origin(url) != _origin(base_url):
        raise ValueError("Fizzy pagination and redirects must stay on the configured origin")
    return urldefrag(url)[0]


class _SameOriginRedirect(HTTPRedirectHandler):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        _require_same_origin(self.base_url, newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _build_url(base_url: str, account_slug: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    base = base_url.rstrip("/")
    if not path.startswith("/"):
        path = "/" + path
    if account_slug:
        account_prefix = f"/{account_slug}"
        if not path.startswith(account_prefix + "/") and path != account_prefix:
            path = account_prefix + path
    return base + path


def _parse_link_next(link_header: str | None) -> str:
    if not link_header:
        return ""
    match = re.search(r"<([^>]+)>;\s*rel=\"next\"", link_header)
    return match.group(1) if match else ""


def _request_json(
    base_url: str,
    account_slug: str,
    token: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> tuple[Any, dict[str, str]]:
    url = _build_url(base_url, account_slug, path)
    if params:
        url += "?" + urlencode(params, doseq=True)

    url = _require_same_origin(base_url, url)
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "xian-tech/roadmap",
    }
    req = Request(url, headers=headers)
    try:
        with build_opener(_SameOriginRedirect(base_url)).open(req, timeout=30) as resp:
            body = resp.read()
            payload = json.loads(body) if body else None
            return payload, dict(resp.headers)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Fizzy API error {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Fizzy API request failed: {exc}") from exc


def get_paginated(
    base_url: str,
    account_slug: str,
    token: str,
    path: str,
    params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    next_url = _build_url(base_url, account_slug, path)
    if params:
        next_url += "?" + urlencode(params, doseq=True)
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    while next_url:
        next_url = _require_same_origin(base_url, next_url)
        if next_url in seen:
            raise ValueError("Fizzy pagination cycle detected")
        if len(seen) >= MAX_PAGES:
            raise ValueError("Fizzy pagination page limit exceeded")
        seen.add(next_url)
        data, headers = _request_json(base_url, account_slug, token, next_url, None)
        if isinstance(data, list):
            results.extend(item for item in data if isinstance(item, dict))
        link = _parse_link_next(
            next((value for key, value in headers.items() if key.lower() == "link"), None)
        )
        next_url = urljoin(next_url, link) if link else ""
    return results


def get_board_columns(
    base_url: str,
    account_slug: str,
    token: str,
    board_id: str,
) -> list[dict[str, Any]]:
    data, _ = _request_json(base_url, account_slug, token, f"/boards/{board_id}/columns")
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def get_board_cards(
    base_url: str,
    account_slug: str,
    token: str,
    board_id: str,
    indexed_by: str | None = None,
) -> list[dict[str, Any]]:
    params: dict[str, Any] = {"board_ids[]": board_id}
    if indexed_by:
        params["indexed_by"] = indexed_by
    return get_paginated(base_url, account_slug, token, "/cards.json", params)
