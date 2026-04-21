#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "latest-writing.json"

SUBSTACK_FEED = "https://abhaskjha.substack.com/feed"
SUBSTACK_ARCHIVE = "https://abhaskjha.substack.com/"
LINKEDIN_NEWSLETTER = "https://www.linkedin.com/newsletters/india-decoded-7226815406265577473/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    )
}


def warn(message: str) -> None:
    print(message, file=sys.stderr)


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = re.sub(r"\s+", " ", unescape(text)).strip()
    return text


def iso_from_rfc822(value: str) -> str:
    dt = parsedate_to_datetime(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_substack_items(limit: int = 6) -> list[dict[str, str]]:
    xml_text = fetch(SUBSTACK_FEED)
    root = ET.fromstring(xml_text)
    items = []
    for item in root.findall("./channel/item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        description = strip_html(item.findtext("description") or "")
        summary = description[:180].rstrip()
        if summary and len(description) > 180:
            summary += "..."
        items.append(
            {
                "title": title,
                "url": link,
                "date": iso_from_rfc822(pub_date) if pub_date else "",
                "summary": summary,
            }
        )
    return items


def unique_linkedin_links(html_text: str, limit: int = 6) -> list[str]:
    matches = re.findall(
        r'class="share-article__title-link"\s+href="(https://www\.linkedin\.com/pulse/[^"]+)"',
        html_text,
    )
    links = []
    seen = set()
    for link in matches:
        if link in seen:
            continue
        seen.add(link)
        links.append(link)
        if len(links) == limit:
            break
    return links


def extract_article_json_ld(html_text: str) -> dict[str, str]:
    scripts = re.findall(
        r'<script[^>]+type="application/ld\+json"[^>]*>\s*(.*?)\s*</script>',
        html_text,
        re.DOTALL,
    )
    for script in scripts:
        try:
            data = json.loads(script)
        except json.JSONDecodeError:
            continue

        candidates = data if isinstance(data, list) else [data]
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("@type") == "Article":
                return candidate
    return {}


def fetch_linkedin_items(limit: int = 6) -> list[dict[str, str]]:
    newsletter_html = fetch(LINKEDIN_NEWSLETTER)
    items = []
    for link in unique_linkedin_links(newsletter_html, limit=limit):
        try:
            article_html = fetch(link)
            metadata = extract_article_json_ld(article_html)
            title_match = re.search(r"<title>(.*?)</title>", article_html, re.DOTALL)
            title = (
                metadata.get("name")
                or metadata.get("headline")
                or strip_html(title_match.group(1) if title_match else link)
            )
            title = re.sub(r"\s*\|\s*LinkedIn\s*$", "", title).strip()
            items.append(
                {
                    "title": title,
                    "url": link,
                    "date": metadata.get("datePublished", ""),
                    "summary": "",
                }
            )
        except Exception as exc:  # noqa: BLE001
            warn(f"Warning: skipping LinkedIn article {link}: {exc}")
    return items


def load_existing_data() -> dict:
    if not DATA_PATH.exists():
        return {}
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def fallback_items(existing_data: dict, key: str) -> list[dict[str, str]]:
    return existing_data.get("sources", {}).get(key, {}).get("items", [])


def safe_items(label: str, loader, existing_items: list[dict[str, str]]) -> list[dict[str, str]]:
    try:
        items = loader()
        if items:
            return items
        if existing_items:
            warn(f"Warning: {label} returned no items. Reusing previous data.")
            return existing_items
        return []
    except Exception as exc:  # noqa: BLE001
        if existing_items:
            warn(f"Warning: {label} refresh failed ({exc}). Reusing previous data.")
            return existing_items
        raise


def main() -> int:
    existing_data = load_existing_data()
    substack_items = safe_items(
        "Substack",
        fetch_substack_items,
        fallback_items(existing_data, "substack"),
    )
    linkedin_items = safe_items(
        "India Decoded",
        fetch_linkedin_items,
        fallback_items(existing_data, "india_decoded"),
    )

    payload = {
        "updated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sources": {
            "substack": {
                "title": "The Urban Stack",
                "url": SUBSTACK_ARCHIVE,
                "items": substack_items,
            },
            "india_decoded": {
                "title": "India Decoded",
                "url": LINKEDIN_NEWSLETTER,
                "items": linkedin_items,
            },
        },
    }

    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
