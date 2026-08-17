#!/usr/bin/env python3
"""
Convert NOVA whitepaper HTML → full Markdown (ZH + EN).

Usage:
  pip install beautifulsoup4 lxml
  python docs/ci/build_md_whitepaper.py
"""

from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[2]
ZH_HTML = ROOT / "NOVA · 数字世界构思白皮书.html"
EN_HTML = ROOT / "docs" / "en" / "whitepaper.html"
ZH_MD = ROOT / "docs" / "zh" / "whitepaper.md"
EN_MD = ROOT / "docs" / "en" / "whitepaper.md"

SKIP_CLASSES = {"copy-btn", "copy-tip"}
SKIP_SELECTORS = ["script", "style", "button"]


def text_inline(el: Tag | NavigableString) -> str:
    if isinstance(el, NavigableString):
        return str(el)
    if not isinstance(el, Tag):
        return ""
    name = el.name or ""
    if name == "br":
        return "\n"
    inner = "".join(text_inline(c) for c in el.children)
    if name in ("strong", "b"):
        return f"**{inner.strip()}**" if inner.strip() else ""
    if name in ("em", "i"):
        return f"*{inner.strip()}*" if inner.strip() else ""
    if name == "code":
        return f"`{inner}`"
    if name == "a":
        href = el.get("href", "")
        label = inner.strip() or href
        if href.startswith("#"):
            return f"[{label}]({href})"
        return f"[{label}]({href})"
    return inner


def table_to_md(table: Tag) -> str:
    rows: list[list[str]] = []
    for tr in table.find_all("tr"):
        cells = []
        for cell in tr.find_all(["th", "td"]):
            cells.append(re.sub(r"\s+", " ", text_inline(cell)).strip().replace("|", "\\|"))
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines = ["| " + " | ".join(rows[0]) + " |"]
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines) + "\n"


def list_to_md(el: Tag, ordered: bool = False) -> str:
    lines = []
    for i, li in enumerate(el.find_all("li", recursive=False), 1):
        prefix = f"{i}. " if ordered else "- "
        body = "".join(convert_block(c, depth=1) for c in li.children if not (isinstance(c, Tag) and c.name in ("ul", "ol")))
        body = body.strip()
        nested = ""
        for sub in li.find_all(["ul", "ol"], recursive=False):
            nested += list_to_md(sub, ordered=sub.name == "ol")
        lines.append(prefix + body)
        if nested:
            lines.append(re.sub(r"(?m)^", "  ", nested.rstrip()))
    return "\n".join(lines) + "\n"


def code_flow_to_md(el: Tag) -> str:
    text = el.get_text()
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.strip().startswith("{") or text.strip().startswith("["):
        return "```json\n" + text.strip() + "\n```\n\n"
    return "```\n" + text.rstrip() + "\n```\n\n"


def block_children_to_md(el: Tag) -> str:
    parts = []
    for child in el.children:
        if isinstance(child, Comment):
            continue
        parts.append(convert_block(child))
    return "".join(parts)


def convert_block(el, depth: int = 0) -> str:
    if isinstance(el, NavigableString):
        s = str(el)
        return s if s.strip() else ""
    if not isinstance(el, Tag):
        return ""

    name = el.name
    classes = set(el.get("class") or [])

    if name in SKIP_SELECTORS:
        return ""
    if classes & SKIP_CLASSES:
        return ""

    if name == "h1":
        return f"# {text_inline(el).strip()}\n\n"
    if name == "h2":
        sid = el.get("id", "")
        title = text_inline(el).strip()
        anchor = f'<a id="{sid}"></a>\n\n' if sid else ""
        return f"{anchor}## {title}\n\n"
    if name == "h3":
        sid = el.get("id", "")
        title = text_inline(el).strip()
        anchor = f'<a id="{sid}"></a>\n\n' if sid else ""
        return f"{anchor}### {title}\n\n"
    if name == "p":
        t = text_inline(el).strip()
        return f"{t}\n\n" if t else ""
    if name == "ul":
        return list_to_md(el, ordered=False)
    if name == "ol":
        return list_to_md(el, ordered=True)
    if name == "table":
        return table_to_md(el) + "\n"
    if name == "div":
        if "code-flow" in classes:
            return code_flow_to_md(el)
        if classes & {"blockquote-charter", "final-quote", "highlight-box", "copyright-box"}:
            inner = block_children_to_md(el).strip()
            if inner:
                quoted = "\n".join("> " + ln if ln else ">" for ln in inner.splitlines())
                return quoted + "\n\n"
        if "table-wrap" in classes:
            return block_children_to_md(el)
        if "toc" in classes:
            return toc_to_md(el)
        if "footer-note" in classes:
            return block_children_to_md(el)
        if "subtitle" in classes or "version-tag" in classes:
            t = text_inline(el).strip()
            return f"*{t}*\n\n" if t else ""
        return block_children_to_md(el)
    if name in ("strong", "em", "code", "a", "span"):
        return text_inline(el)
    return block_children_to_md(el)


def toc_to_md(el: Tag) -> str:
    title = "文档目录" if re.search(r"[\u4e00-\u9fff]", el.get_text()[:20]) else "Table of Contents"
    lines = [f"## {title}\n"]
    for a in el.find_all("a", href=True):
        href = a["href"]
        label = a.get_text(strip=True)
        if href.startswith("#") and label:
            lines.append(f"- [{label}]({href})")
    return "\n".join(lines) + "\n\n"


def normalize_md_paths(md: str, out_path: Path) -> str:
    """Fix repo-root-relative hrefs for Markdown file location."""
    if out_path.parent.name == "zh":
        md = re.sub(r"\]\(index\.html\)", "](../../index.html)", md)
        md = re.sub(r"\]\(docs/en/whitepaper\.html\)", "](../en/whitepaper.md)", md)
        md = re.sub(r"\]\(docs/index\.html\)", "](../index.html)", md)
        md = re.sub(r"\]\(docs/", "](../", md)
    elif out_path.parent.name == "en":
        md = re.sub(r"\]\(whitepaper\.html\)", "](whitepaper.md)", md)
        md = re.sub(r"\]\(docs/en/whitepaper\.html\)", "](whitepaper.md)", md)
        md = re.sub(r"\]\(docs/en/", "](./", md)
        md = re.sub(r"\]\(docs/", "](../", md)
        md = re.sub(
            r"\]\(\../../NOVA%20%C2%B7%20%E6%95%B0%E5%AD%97%E4%B8%96%E7%95%8C%E6%9E%84%E6%80%9D%E7%99%BD%E7%9A%AE%E4%B9%A6\.html\)",
            "](../zh/whitepaper.md)",
            md,
        )
    return md


def html_to_md(html_path: Path, lang: str) -> str:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    container = soup.find("div", class_="container")
    if not container:
        raise SystemExit(f"No .container in {html_path}")

    # skip first highlight nav box in body output (keep in md as blockquote)
    parts = []
    for child in container.children:
        if isinstance(child, Comment):
            continue
        if isinstance(child, Tag) and child.name == "div":
            style = child.get("style", "")
            if "copy-btn" in child.get_text() or (child.find("button", class_="copy-btn")):
                continue
        parts.append(convert_block(child))

    body = "".join(parts)
    body = re.sub(r"\n{3,}", "\n\n", body)

    if lang == "zh":
        header = """---
title: "NOVA · 数字世界构思白皮书"
version: "V1.7.1"
lang: zh-CN
author: rainzheng
license: "CC BY-NC-ND 4.0"
source_html: "../../NOVA · 数字世界构思白皮书.html"
---

"""
    else:
        header = """---
title: "NOVA · Digital Civilization Whitepaper"
version: "V1.7.1"
lang: en
author: rainzheng
license: "CC BY-NC-ND 4.0"
source_html: "./whitepaper.html"
disclaimer: "EN-01 — Chinese edition is authoritative for legal interpretation."
---

"""

    footer = """
---

**© 2026 rainzheng** · irainzheng@163.com · CC BY-NC-ND 4.0

*Generated from HTML via `docs/ci/build_md_whitepaper.py`. For authoritative layout, use the HTML edition.*
"""
    return header + body.strip() + footer


def write_md(html_path: Path, out_path: Path, lang: str) -> None:
    md = html_to_md(html_path, lang)
    md = normalize_md_paths(md, out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(f"{'ZH' if lang == 'zh' else 'EN'}: {out_path} ({len(md)//1024} KB, {md.count(chr(10))} lines)")


def main() -> None:
    write_md(ZH_HTML, ZH_MD, "zh")
    write_md(EN_HTML, EN_MD, "en")


if __name__ == "__main__":
    main()
