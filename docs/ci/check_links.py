#!/usr/bin/env python3
"""Validate links in NOVA HTML/Markdown files."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
HTML_HREF = re.compile(r'href=["\']([^"\']+)["\']', re.I)
MD_LINK = re.compile(r'\[[^\]]*\]\(([^)]+)\)')
ID_ATTR = re.compile(r'\bid=["\']([^"\']+)["\']', re.I)

# Paths authored from repo root but used inside docs/en/whitepaper.html
EN_ROOT_ALIASES = {
    "docs/en/whitepaper.html": "whitepaper.html",
}


def collect_ids(html: str) -> set[str]:
    return set(ID_ATTR.findall(html))


def is_external(url: str) -> bool:
    p = urlparse(url)
    return bool(p.scheme) or url.startswith("//")


def resolve_href(path: Path, url: str) -> Path:
    parsed = urlparse(url)
    target = unquote(parsed.path)
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return (path.parent / target).resolve()


def check_file(path: Path, issues: list) -> None:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)

    if path.suffix.lower() == ".html":
        links = HTML_HREF.findall(text)
        ids = collect_ids(text)
    else:
        links = MD_LINK.findall(text)
        ids = set()

    for raw in links:
        url = raw.strip()
        if not url or is_external(url):
            continue
        if url.startswith("#"):
            anchor = unquote(url[1:])
            if ids and anchor not in ids:
                issues.append((str(rel), url, "missing anchor in same file"))
            continue

        parsed = urlparse(url)
        resolved = resolve_href(path, url)

        if not resolved.exists():
            # allow docs/en/* paths when checking from docs/en/whitepaper.html context
            alias = EN_ROOT_ALIASES.get(url)
            if alias and (path.parent / alias).resolve().exists():
                continue
            issues.append(
                (str(rel), url, f"target not found: {resolved.relative_to(ROOT) if resolved.is_relative_to(ROOT) else resolved}")
            )

        if parsed.fragment and resolved.suffix.lower() == ".html" and resolved.exists():
            target_ids = collect_ids(resolved.read_text(encoding="utf-8"))
            if unquote(parsed.fragment) not in target_ids:
                issues.append((str(rel), url, f"missing anchor #{parsed.fragment} in {resolved.relative_to(ROOT)}"))


def main() -> int:
    issues: list[tuple[str, str, str]] = []
    files = list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.md"))
    for f in sorted(files):
        if ".git" in f.parts:
            continue
        check_file(f, issues)

    for name in ["NOVA · 数字世界构思白皮书.html", "docs/en/whitepaper.html"]:
        p = ROOT / name
        html = p.read_text(encoding="utf-8")
        ids = collect_ids(html)
        for aid in re.findall(r'href="#(sec-[^"]+)"', html):
            if aid not in ids:
                issues.append((name, f"#{aid}", "TOC anchor missing in document"))

    if not issues:
        print(f"PASS: checked {len(files)} files, no broken links")
        return 0

    print(f"FAIL: {len(issues)} issue(s)\n")
    for src, url, msg in issues:
        print(f"  [{src}] {url}\n    -> {msg}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
