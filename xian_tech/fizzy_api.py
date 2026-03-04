"""Lightweight Fizzy API helper (no client dependency)."""
from __future__ import annotations

import json
import re

from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


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

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "xian-tech/roadmap",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=30) as resp:
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
    data, headers = _request_json(base_url, account_slug, token, path, params)
    results: list[dict[str, Any]] = []
    if isinstance(data, list):
        results.extend([item for item in data if isinstance(item, dict)])

    next_url = _parse_link_next(headers.get("Link"))
    while next_url:
        data, headers = _request_json(base_url, account_slug, token, next_url, None)
        if isinstance(data, list):
            results.extend([item for item in data if isinstance(item, dict)])
        next_url = _parse_link_next(headers.get("Link"))

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
    # Fizzy API/CLI use board_ids[] list parameters.
    params: dict[str, Any] = {"board_ids[]": board_id}
    if indexed_by:
        params["indexed_by"] = indexed_by
    results = get_paginated(base_url, account_slug, token, "/cards.json", params)
    if results:
        return results
    # Backward compatibility for older/self-hosted deployments.
    fallback_params: dict[str, Any] = {"board_ids": board_id}
    if indexed_by:
        fallback_params["indexed_by"] = indexed_by
    return get_paginated(base_url, account_slug, token, "/cards.json", fallback_params)
