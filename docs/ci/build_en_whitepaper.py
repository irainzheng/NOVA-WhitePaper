#!/usr/bin/env python3
"""
Build full English whitepaper from Chinese HTML.
Preserves section IDs, tables, and code blocks; translates prose.

Usage:
  pip install beautifulsoup4 deep-translator pyyaml
  python docs/ci/build_en_whitepaper.py
"""

from __future__ import annotations

import json
import re
import time
import urllib3
from pathlib import Path

import requests
from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from deep_translator import GoogleTranslator

# Corporate proxy / self-signed MITM: allow Google Translate endpoint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
_orig_get = requests.get
requests.get = lambda *args, **kwargs: _orig_get(*args, verify=False, **kwargs)  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "NOVA · 数字世界构思白皮书.html"
OUT = ROOT / "docs" / "en" / "whitepaper.html"
CACHE = Path(__file__).resolve().parent / ".translation_cache.json"

CJK = re.compile(r"[\u4e00-\u9fff]")
SKIP_TAGS = {"style", "script", "code"}
SEP = "\n###NOVA_SEP###\n"
ASCII_ONLY = re.compile(r"^[\x00-\x7f\s\d\.\->│┌┐└┘├┤─=]+$")


def load_cache() -> dict[str, str]:
    if CACHE.is_file():
        raw = json.loads(CACHE.read_text(encoding="utf-8"))
        return {k: v for k, v in raw.items() if v and v.strip() != k.strip() and not _needs_translation(v)}
    return {}


def _needs_translation(text: str) -> bool:
    return bool(CJK.search(text))


def save_cache(cache: dict[str, str]) -> None:
    CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def translate_one(text: str, translator: GoogleTranslator, cache: dict[str, str]) -> str:
    key = text.strip()
    if not key or not _needs_translation(text):
        return text
    if key in cache:
        return cache[key]

    payload = text
    for attempt in range(4):
        try:
            out = translator.translate(payload)
            if out and out.strip() != key:
                cache[key] = out
                return out
        except Exception:
            time.sleep(0.8 * (attempt + 1))
    cache[key] = text
    return text


def translate_batch(texts: list[str], translator: GoogleTranslator, cache: dict[str, str]) -> list[str]:
    results: list[str | None] = [None] * len(texts)
    pending: list[tuple[int, str]] = []

    for i, t in enumerate(texts):
        if not _needs_translation(t):
            results[i] = t
            continue
        k = t.strip()
        if k in cache:
            results[i] = cache[k]
        else:
            pending.append((i, t))

    i = 0
    while i < len(pending):
        chunk: list[tuple[int, str]] = []
        clen = 0
        while i < len(pending) and clen < 2800:
            chunk.append(pending[i])
            clen += len(pending[i][1]) + len(SEP)
            i += 1

        joined = SEP.join(t for _, t in chunk)
        translated = None
        for attempt in range(4):
            try:
                translated = translator.translate(joined)
                parts = translated.split("###NOVA_SEP###")
                if len(parts) == len(chunk):
                    break
            except Exception:
                time.sleep(0.8 * (attempt + 1))
            translated = None

        if translated and len(translated.split("###NOVA_SEP###")) == len(chunk):
            for (idx, orig), part in zip(chunk, translated.split("###NOVA_SEP###")):
                cache[orig.strip()] = part
                results[idx] = part
        else:
            for idx, orig in chunk:
                results[idx] = translate_one(orig, translator, cache)
        time.sleep(0.25)

    return [r if r is not None else texts[j] for j, r in enumerate(results)]


def should_skip_node(node: NavigableString, chain: list[str]) -> bool:
    text = str(node)
    if not text.strip():
        return True
    if not _needs_translation(text):
        return True
    if any(t in SKIP_TAGS for t in chain):
        return True
    if chain and chain[-1] == "code-flow":
        if ASCII_ONLY.match(text.strip()):
            return True
        if text.strip().startswith("{") or '"asp_version"' in text:
            return True
    return False


def collect_nodes(soup: BeautifulSoup) -> list[tuple[NavigableString, list[str]]]:
    out: list[tuple[NavigableString, list[str]]] = []

    def walk(el, chain: list[str]) -> None:
        if isinstance(el, Comment):
            return
        if isinstance(el, NavigableString):
            if isinstance(el.parent, Tag):
                out.append((el, chain))
            return
        if not isinstance(el, Tag):
            return
        name = el.name or ""
        walk_chain = chain + ([name] if name else [])
        for child in el.children:
            walk(child, walk_chain)

    walk(soup, [])
    return out


ZH_MAIN = "../../NOVA%20%C2%B7%20%E6%95%B0%E5%AD%97%E4%B8%96%E7%95%8C%E6%9E%84%E6%80%9D%E7%99%BD%E7%9A%AE%E4%B9%A6.html"


def en_relative_href(path: str) -> str:
    """Rewrite repo-root docs/ paths for docs/en/whitepaper.html."""
    path = path.strip()
    if path.startswith("docs/en/"):
        rest = path[len("docs/en/") :]
        return rest or "whitepaper.html"
    if path.startswith("docs/"):
        return "../" + path[len("docs/") :]
    return path


def fix_en_hrefs(soup: BeautifulSoup) -> None:
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("#") or href.startswith("http") or href.startswith("mailto:"):
            continue
        if href.startswith("docs/"):
            a["href"] = en_relative_href(href)


def post_process(soup: BeautifulSoup) -> None:
    if soup.html:
        soup.html["lang"] = "en"
    if soup.title:
        soup.title.string = "NOVA · Digital Civilization Whitepaper (Full English Edition)"

    container = soup.find("div", class_="container")
    if container:
        banner = soup.new_tag("div")
        banner["class"] = "highlight-box"
        banner["style"] = "margin-bottom:20px;"
        banner.append("Full English Edition · V1.7.1 — Official Chinese text remains authoritative for legal interpretation (EN-01). ")
        banner.append("Chinese edition: ")
        zh_link = soup.new_tag("a", href=ZH_MAIN)
        zh_link.string = "NOVA · 数字世界构思白皮书.html"
        banner.append(zh_link)
        banner.append(" · ")
        home = soup.new_tag("a", href="../../index.html")
        home.string = "Language hub"
        banner.append(home)
        container.insert(0, banner)

    btn = soup.find("button", class_="copy-btn")
    if btn:
        btn.string = "📋 Copy full text"
    tip = soup.find("span", class_="copy-tip")
    if tip:
        tip.string = "Paste into Word / Notion to save"

    h1 = soup.find("h1")
    if h1 and _needs_translation(h1.get_text()):
        h1.string = "NOVA · Digital Civilization Whitepaper"

    for sid, title in [
        ("sec-en", "0.8 English Edition Notice"),
        ("sec-en-html", "0.9 Bilingual Sync & CI"),
    ]:
        h = soup.find(id=sid)
        if h:
            h.string = title

    fix_en_hrefs(soup)


def main() -> None:
    print(f"Reading: {SRC.name}")
    html = SRC.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    cache = load_cache()
    translator = GoogleTranslator(source="zh-CN", target="en")

    nodes = collect_nodes(soup)
    texts: list[str] = []
    refs: list[NavigableString] = []
    for node, chain in nodes:
        if should_skip_node(node, chain):
            continue
        texts.append(str(node))
        refs.append(node)

    print(f"Translating {len(texts)} segments (cache hit: {sum(1 for t in texts if t.strip() in cache)})...")
    translated = translate_batch(texts, translator, cache)

    for node, new_text in zip(refs, translated):
        node.replace_with(new_text)

    save_cache(cache)
    post_process(soup)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    out_html = soup.prettify(formatter="html")
    OUT.write_text(out_html, encoding="utf-8")

    body = OUT.read_text(encoding="utf-8")
    remaining = len(CJK.findall(body))
    print(f"Written: {OUT} ({len(body) // 1024} KB, {body.count(chr(10))} lines)")
    print(f"Remaining CJK chars: {remaining}")
    print(f"Cache entries: {len(cache)}")


if __name__ == "__main__":
    main()
