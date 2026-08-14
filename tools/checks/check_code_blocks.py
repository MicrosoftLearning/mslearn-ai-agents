#!/usr/bin/env python3
"""Check that every ```python block in the lab instructions is valid Python.

Learners paste these blocks straight into a file, so a syntax error - almost
always a bad indent - breaks the lab. Two fixes on main ("fix fence
indentation", "fix code sample indentation") were exactly this class of bug.

Normalization matters here. The blocks are snippets, not programs:

  1. They are indented to sit inside a function body, so the whole block is
     dedented first. Without this, 134 of 148 blocks would report false
     positives.
  2. Some intentionally end on an open block - a `with` or `def` whose body the
     lab adds in a later step. If parsing fails *only* because a block opener
     has no body, a `pass` is appended and it is retried.

A genuine syntax error - typo, unbalanced bracket, or bad indent *within* the
snippet - still fails, which is the point.
"""

import ast
import re
import textwrap

from common import Reporter, lab_pages, main_guard

FENCE = re.compile(r"(?ms)^[ \t]*```python[ \t]*\r?\n(.*?)^[ \t]*```")
INCOMPLETE_BLOCK = "expected an indented block"


def close_open_block(code: str) -> str:
    """Give a trailing block opener a body so a fragment can be parsed."""
    lines = [l for l in code.rstrip().split("\n") if l.strip()]
    if not lines:
        return code
    last = lines[-1]
    indent = len(last) - len(last.lstrip())
    if last.rstrip().endswith(":"):
        indent += 4
    return code.rstrip() + "\n" + " " * indent + "pass\n"


def parse_snippet(code: str):
    """Return None if the snippet is acceptable, else a SyntaxError to report."""
    dedented = textwrap.dedent(code)
    try:
        ast.parse(dedented)
        return None
    except SyntaxError as first:
        if INCOMPLETE_BLOCK not in str(first):
            return first

    try:
        ast.parse(close_open_block(dedented))
        return None
    except SyntaxError as second:
        return second


def check() -> int:
    r = Reporter("python code blocks")

    for path in lab_pages():
        text = path.read_text(encoding="utf-8")
        for match in FENCE.finditer(text):
            r.checked += 1
            err = parse_snippet(match.group(1))
            if err is None:
                continue

            # Line of the ``` fence, plus the offset reported inside the block.
            fence_line = text[: match.start()].count("\n") + 1
            line = fence_line + (err.lineno or 1)
            reason = str(err).split("(")[0].strip()
            r.add(path, f"invalid Python in code block: {reason}", line)

    return r.finish("blocks")


if __name__ == "__main__":
    main_guard(check)
