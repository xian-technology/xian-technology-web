from __future__ import annotations

import importlib
import pkgutil
from typing import Any, Iterable

from .data import (
    CORE_COMPONENTS,
    ECOSYSTEM_INITIATIVES,
    TECHNOLOGY_TRACKS,
    _slugify,
)
from . import pages


def _clean_text(value: Any) -> str:
    return " ".join(str(value).split()).strip()


def _normalize_keywords(value: Any) -> list[str]:
    if value is None:
        return []
    keywords = [value] if isinstance(value, str) else list(value)
    normalized: list[str] = []
    seen: set[str] = set()
    for keyword in keywords:
        cleaned = _clean_text(keyword)
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        normalized.append(lowered)
    return normalized


def _normalize_entry(entry: dict[str, Any]) -> dict[str, Any]:
    title = _clean_text(entry["title"])
    category = _clean_text(entry.get("category", "General"))
    href = _clean_text(entry.get("href", "/"))
    return {
        "id": _clean_text(entry.get("id", f"{_slugify(category)}-{_slugify(title)}")),
        "title": title,
        "subtitle": _clean_text(entry.get("subtitle", "")),
        "category": category,
        "badge": _clean_text(entry.get("badge", "Section")),
        "href": href,
        "external": bool(entry.get("external", href.startswith(("http://", "https://", "mailto:")))),
        "keywords": _normalize_keywords(entry.get("keywords", [])),
    }


def _normalize_sections(sections: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_normalize_entry(section) for section in sections]


def _normalize_entries(entries: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_normalize_entry(entry) for entry in entries]


def _ensure_unique_ids(entries: Iterable[dict[str, Any]]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for entry in entries:
        entry_id = entry["id"]
        if entry_id in seen:
            duplicates.add(entry_id)
        else:
            seen.add(entry_id)
    if duplicates:
        raise ValueError(
            "Duplicate search entry ids found: "
            + ", ".join(sorted(duplicates))
            + ". Add explicit unique ids to SEARCH_SECTIONS entries."
        )


def _discover_page_sections() -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    for module_info in sorted(pkgutil.iter_modules(pages.__path__), key=lambda info: info.name):
        module = importlib.import_module(f"{pages.__name__}.{module_info.name}")
        page_sections = getattr(module, "SEARCH_SECTIONS", None)
        if isinstance(page_sections, list):
            sections.extend(page_sections)
    return sections


def _build_search_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    page_sections = _discover_page_sections()
    entries.extend(_normalize_sections(page_sections))

    for track in TECHNOLOGY_TRACKS:
        entries.append(
            {
                "id": f"technology-{_slugify(track['title'])}",
                "title": track["title"],
                "subtitle": track["description"],
                "category": "Technology",
                "badge": "Track",
                "href": "/contracting",
                "external": False,
                "keywords": track["points"],
            }
        )

    entries.append(
        {
            "id": "technology-get-started",
            "title": "Deploy your first smart contract",
            "subtitle": "pip install xian-py → xian init → xian deploy",
            "category": "Technology",
            "badge": "Guide",
            "href": "/contracting",
            "external": False,
            "keywords": ["Get started", "Terminal prompt", "Documentation"],
        }
    )

    for item in ECOSYSTEM_INITIATIVES:
        entries.append(
            {
                "id": f"ecosystem-{_slugify(item['title'])}",
                "title": item["title"],
                "subtitle": item["description"],
                "category": "Developers",
                "badge": "Program",
                "href": "/ecosystem",
                "external": False,
                "keywords": item["links"],
            }
        )

    entries.append(
        {
            "id": "ecosystem-partner",
            "title": "Partner With Us",
            "subtitle": "Collaboration pathways for researchers, builders, and educators.",
            "category": "Developers",
            "badge": "CTA",
            "href": "/ecosystem",
            "external": False,
            "keywords": ["Request partnership", "Collaboration"],
        }
    )

    entries += [
        {
            "id": "docs-xian",
            "title": "View Documentation",
            "subtitle": "Open the official Xian documentation site.",
            "category": "Resources",
            "badge": "Docs",
            "href": "https://docs.xian.technology",
            "external": True,
            "keywords": ["Documentation", "Guides", "Tutorials"],
        },
        {
            "id": "github-org",
            "title": "GitHub Organization",
            "subtitle": "Review repositories across the Xian Technology stack.",
            "category": "Resources",
            "badge": "Code",
            "href": "https://github.com/xian-technology",
            "external": True,
            "keywords": ["GitHub", "Repositories", "Code"],
        },
        {
            "id": "contact-foundation",
            "title": "Email the Foundation",
            "subtitle": "foundation@xian.technology — reach the core team.",
            "category": "Resources",
            "badge": "Contact",
            "href": "mailto:foundation@xian.technology",
            "external": True,
            "keywords": ["Contact", "Foundation", "Email"],
        },
    ]

    for component in CORE_COMPONENTS:
        entries.append(
            {
                "id": f"stack-{_slugify(component['title'])}",
                "title": component["title"],
                "subtitle": component["description"],
                "category": "Stack",
                "badge": "Component",
                "href": component["href"],
                "external": False,
                "keywords": [component["title"], component["description"]],
            }
        )

    entries = _normalize_entries(entries)
    _ensure_unique_ids(entries)
    return entries


SEARCH_ENTRIES = _build_search_entries()


__all__ = ["SEARCH_ENTRIES"]
