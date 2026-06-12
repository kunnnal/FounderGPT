"""Helpers for extracting short citations from markdown knowledge files."""

from __future__ import annotations

from pathlib import Path


def parse_markdown_excerpt(path: Path) -> tuple[str, str]:
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return path.stem.replace("_", " ").title(), ""

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    title = path.stem.replace("_", " ").title()
    if lines and lines[0].startswith("#"):
        title = lines[0].lstrip("#").strip()
        lines = lines[1:]

    snippet = " ".join(lines[:3]).strip()
    return title, snippet[:240]

