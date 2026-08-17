#!/usr/bin/env python3
"""
NOVA whitepaper EN/ZH chapter sync checker — V1.7.1
Usage: python docs/ci/sync_check.py
Exit 0 if all ZH section IDs exist in EN with non-empty content.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as e:
    raise SystemExit("Install PyYAML: pip install pyyaml") from e

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = Path(__file__).resolve().parent / "chapter-manifest.yaml"
SEC_ID = re.compile(r'\bid="(sec-[^"]+)"')


def load_manifest() -> dict:
    with MANIFEST.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_section(html: str, section_id: str) -> str | None:
    pattern = rf'<h[23][^>]*\bid="{re.escape(section_id)}"[^>]*>.*?(?=<h[23]\s|$)'
    m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
    if not m:
        pattern2 = rf'\bid="{re.escape(section_id)}"[^>]*>(.*?)(?=\bid="sec-|\Z)'
        m = re.search(pattern2, html, re.DOTALL | re.IGNORECASE)
    return m.group(0) if m else None


def strip_tags(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def all_section_ids(html: str) -> list[str]:
    return SEC_ID.findall(html)


def main() -> int:
    manifest = load_manifest()
    ci_dir = Path(__file__).resolve().parent
    en_path = (ci_dir / manifest["en_mirror"]).resolve()
    zh_path = (ci_dir / manifest["zh_source"]).resolve()

    if not en_path.is_file():
        print(f"FAIL: EN edition not found: {en_path}")
        return 1
    if not zh_path.is_file():
        print(f"WARN: ZH source not found: {zh_path}")

    en_html = en_path.read_text(encoding="utf-8")
    zh_html = zh_path.read_text(encoding="utf-8") if zh_path.is_file() else ""

    zh_ids = all_section_ids(zh_html)
    en_ids = set(all_section_ids(en_html))
    missing_ids = [sid for sid in zh_ids if sid not in en_ids]

    missing = []
    empty = []
    for ch in manifest["chapters"]:
        if not ch.get("required", False):
            continue
        sid = ch["id"]
        block = extract_section(en_html, sid)
        if block is None:
            missing.append(sid)
            continue
        if len(strip_tags(block)) < 20:
            empty.append(sid)

    print(f"=== NOVA Sync Check v{manifest['version']} ===")
    print(f"EN edition: {en_path.name}")
    print(f"ZH section IDs: {len(zh_ids)} | EN section IDs: {len(en_ids)}")
    print(f"Manifest required chapters: {sum(1 for c in manifest['chapters'] if c.get('required'))}")

    if missing_ids:
        print(f"\nMISSING ZH→EN section IDs ({len(missing_ids)}):")
        for sid in missing_ids[:20]:
            print(f"  - {sid}")
        if len(missing_ids) > 20:
            print(f"  ... and {len(missing_ids) - 20} more")

    if missing:
        print(f"\nMISSING manifest anchors ({len(missing)}):")
        for sid in missing:
            print(f"  - {sid}")
    if empty:
        print(f"\nEMPTY sections ({len(empty)}):")
        for sid in empty:
            print(f"  - {sid}")

    if missing_ids or missing or empty:
        print("\nResult: FAIL")
        return 1

    print("\nResult: PASS — full section parity + manifest chapters OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
