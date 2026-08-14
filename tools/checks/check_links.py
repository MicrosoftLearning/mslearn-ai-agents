#!/usr/bin/env python3
"""Check that relative links and image references in the lab pages resolve.

Covers the two ways lab navigation breaks:

  - a task page links to a sibling page that was renamed or moved
  - a page references a screenshot under ../Media that no longer exists

External links (http/https) and in-page anchors are not checked; that needs
network access and is noisy in CI.
"""

import re
from urllib.parse import unquote

from common import Reporter, lab_pages, main_guard, repo_root

LINK = re.compile(r"\[[^\]]*\]\(\s*([^)\s]+?)\s*(?:\"[^\"]*\")?\)")
CSS_URL = re.compile(r"url\(\s*[\"']?([^\"')]+)[\"']?\s*\)")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "//", "{{", "{%")

# Code regions must be masked before scanning. Python such as
#   local_functions[item.name](**kwargs)
# is otherwise indistinguishable from a markdown link.
FENCED = re.compile(r"(?ms)^[ \t]*```.*?^[ \t]*```")
INLINE_CODE = re.compile(r"`[^`\n]*`")


def mask_code(text: str) -> str:
    """Blank out code regions, preserving length and newlines so offsets hold."""

    def blank(m: re.Match) -> str:
        return "".join("\n" if ch == "\n" else " " for ch in m.group(0))

    return INLINE_CODE.sub(blank, FENCED.sub(blank, text))


def candidates(text: str):
    scannable = mask_code(text)
    for m in LINK.finditer(scannable):
        yield m.group(1), m.start()
    for m in CSS_URL.finditer(scannable):
        yield m.group(1), m.start()


def check() -> int:
    r = Reporter("links and media")
    root = repo_root()

    for path in lab_pages():
        text = path.read_text(encoding="utf-8")
        for target, offset in candidates(text):
            if target.startswith(SKIP_PREFIXES):
                continue

            clean = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not clean:
                continue

            r.checked += 1
            resolved = (path.parent / clean).resolve()

            if resolved.exists():
                continue

            # Jekyll serves .md as .html; accept a link written either way.
            if resolved.suffix == ".html" and resolved.with_suffix(".md").exists():
                continue

            line = text[:offset].count("\n") + 1
            try:
                shown = resolved.relative_to(root).as_posix()
            except ValueError:
                shown = clean
            r.add(path, f"link target does not exist: {target} -> {shown}", line)

    return r.finish("references")


if __name__ == "__main__":
    main_guard(check)
