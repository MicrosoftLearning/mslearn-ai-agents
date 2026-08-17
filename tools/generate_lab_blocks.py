#!/usr/bin/env python3
"""Write the generated blocks in the lab pages from task frontmatter.

The lab instruction pages are consumed directly by platforms that never run
Liquid - GitHub's own markdown renderer among them, where a `{% include %}`
shows up literally where the content should be. So these pages stay plain
markdown, and the generated parts are written into them here instead.

Two blocks are generated:

  task-table    the "Lab at a glance" table on each lab landing page
  gated-notice  the access warning at the top of a task that needs
                permissions or licensing many learners won't have

Both are delimited by HTML comments, which are invisible in every renderer:

    <!-- BEGIN GENERATED: task-table -->
    ...
    <!-- END GENERATED: task-table -->

    python tools/generate_lab_blocks.py           # rewrite the blocks
    python tools/generate_lab_blocks.py --check   # fail if any is stale

Web-only pages (workshop.md, explore.md, labs.json) still use Liquid directly.
They are never consumed as raw markdown, so there is nothing to work around.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONSOLIDATED = ROOT / "Instructions" / "Consolidated"
FRONTMATTER = re.compile(r"^---\r?\n(.*?\r?\n)---\r?\n", re.S)

DO_NOT_EDIT = "do not edit by hand; run: python tools/generate_lab_blocks.py"


def block_markers(name: str) -> tuple[str, str]:
    return (
        f"<!-- BEGIN GENERATED: {name} - {DO_NOT_EDIT} -->",
        f"<!-- END GENERATED: {name} -->",
    )


def load_pages() -> dict[str, dict]:
    pages = {}
    for path in sorted(CONSOLIDATED.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        m = FRONTMATTER.match(text)
        if not m:
            continue
        data = yaml.safe_load(m.group(1)) or {}
        pages[path.name] = {"path": path, "lab": data.get("lab") or {}}
    return pages


def bars(difficulty: int | None) -> str:
    if not difficulty:
        return ""
    return "▰" * difficulty + "▱" * (5 - difficulty)


def humanise(minutes: int) -> str:
    hours, mins = divmod(minutes, 60)
    if hours and mins:
        return f"{hours} hour{'s' if hours > 1 else ''} {mins} minutes"
    if hours:
        return f"{hours} hour{'s' if hours > 1 else ''}"
    return f"{mins} minutes"


def render_task_table(lab_id: str, pages: dict[str, dict]) -> str:
    tasks = sorted(
        (p for p in pages.values() if p["lab"].get("parent") == lab_id),
        key=lambda p: p["lab"].get("order", 0),
    )
    if not tasks:
        raise SystemExit(f"no task pages found for lab '{lab_id}'")

    core_total = sum(t["lab"].get("duration") or 0 for t in tasks if t["lab"].get("section") == "core")
    full_total = sum(t["lab"].get("duration") or 0 for t in tasks)

    lines = ["| Section | Task | Level | Time |", "| --- | --- | --- | --- |"]
    gated = False

    for t in tasks:
        lab = t["lab"]
        if lab.get("section") == "setup":
            continue
        section = "**Core**" if lab.get("section") == "core" else "*Optional*"
        lock = " 🔒" if lab.get("access") == "gated" else ""
        if lock:
            gated = True
        link = f"[{lab['title']}]({t['path'].name})"
        lines.append(
            f"| {section} | {link}{lock} | {bars(lab.get('difficulty'))} L{lab.get('level')} "
            f"| ~{lab.get('duration')} min |"
        )

    lines.append("")
    lines.append(
        f"**Core tasks:** about **{core_total} minutes**. **Full lab**, including every "
        f"optional task: about **{humanise(full_total)}**."
    )

    if gated:
        lines += [
            "",
            "> 🔒 Tasks marked with a lock need access your account may not have. Each one opens",
            "> with a quick check and tells you what to do if you don't have it — nothing else in",
            "> this lab depends on them.",
        ]

    return "\n".join(lines)


def render_gated_notice(lab: dict) -> str:
    skip = (
        "**Don't have it?** Skip this task. Nothing else in this lab depends on it, and you "
        "can still read through the steps to see how it works."
    )
    lines = [
        "> ### Check your access before you start",
        ">",
        f"> **This task needs:** {lab['requires']}.",
        ">",
        f"> {lab['verify']}",
    ]
    if lab.get("verify_command"):
        lines += ["", "```", lab["verify_command"], "```", "", f"> {skip}"]
    else:
        lines += [">", f"> {skip}"]
    return "\n".join(lines)


def has_block(text: str, name: str) -> bool:
    return f"<!-- BEGIN GENERATED: {name}" in text


def replace_block(text: str, name: str, content: str, path: Path) -> str:
    begin, end = block_markers(name)
    pattern = re.compile(
        r"<!-- BEGIN GENERATED: " + re.escape(name) + r"\b.*?-->.*?<!-- END GENERATED: "
        + re.escape(name) + r" -->",
        re.S,
    )
    replacement = f"{begin}\n{content}\n{end}"
    if not pattern.search(text):
        raise SystemExit(
            f"{path.name}: expected a '{name}' block. Add the markers where it belongs:\n"
            f"  {begin}\n  {end}"
        )
    return pattern.sub(lambda _m: replacement, text, count=1)


def build(pages: dict[str, dict]) -> dict[Path, str]:
    """Return the intended content of every page that carries a generated block."""
    wanted: dict[Path, str] = {}

    for page in pages.values():
        lab = page["lab"]
        path = page["path"]
        text = path.read_text(encoding="utf-8")
        updated = text

        # Every lab landing page must have a task table, so a missing marker
        # here is an error - a new lab should not ship without one.
        if lab.get("type") == "lab":
            updated = replace_block(updated, "task-table", render_task_table(lab["id"], pages), path)

        # The access notice is editorial: the author decides where it goes, and
        # some gated tasks may carry the warning in their own prose instead. So
        # it is generated where the markers appear, and absence is not an error.
        if lab.get("access") == "gated" and has_block(updated, "gated-notice"):
            for key in ("requires", "verify"):
                if not lab.get(key):
                    raise SystemExit(f"{path.name}: access is gated but lab.{key} is missing")
            updated = replace_block(updated, "gated-notice", render_gated_notice(lab), path)

        if updated != text:
            wanted[path] = updated

    return wanted


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report stale blocks, change nothing")
    args = ap.parse_args()

    pages = load_pages()
    wanted = build(pages)

    if not args.check:
        for path, content in wanted.items():
            path.write_bytes(content.encode("utf-8"))
        print(f"generated blocks: {len(wanted)} file(s) updated")
        for path in wanted:
            print("  ", path.relative_to(ROOT).as_posix())
        return 0

    if not wanted:
        print(f"generated blocks: OK - {len(pages)} page(s) checked")
        return 0

    for path, content in wanted.items():
        rel = path.relative_to(ROOT).as_posix()
        sys.stdout.writelines(
            difflib.unified_diff(
                path.read_text(encoding="utf-8").splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=f"{rel} (in repo)",
                tofile=f"{rel} (expected)",
                n=1,
            )
        )
    print(f"\ngenerated blocks: STALE - {len(wanted)} file(s)")
    print("Run: python tools/generate_lab_blocks.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
