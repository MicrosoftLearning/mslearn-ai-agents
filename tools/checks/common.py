"""Shared helpers for the lab content checks.

Every check script reports problems the same way so the workflow output and the
GitHub PR annotations stay consistent.
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

# Directories holding lab instruction pages.
LAB_DIRS = ("Instructions/Exercises", "Instructions/Consolidated")

FRONTMATTER = re.compile(r"^---\r?\n(.*?\r?\n)---\r?\n", re.S)


def repo_root() -> Path:
    """Repo root, assuming this file lives at <root>/tools/checks/."""
    return Path(__file__).resolve().parents[2]


def lab_pages(root: Path | None = None) -> list[Path]:
    root = root or repo_root()
    pages: list[Path] = []
    for d in LAB_DIRS:
        pages.extend(sorted((root / d).glob("*.md")))
    return pages


def split_frontmatter(text: str) -> tuple[str | None, str]:
    m = FRONTMATTER.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


@dataclass
class Problem:
    path: Path
    line: int | None
    message: str


class Reporter:
    """Collects problems and prints them as GitHub Actions annotations."""

    def __init__(self, name: str):
        self.name = name
        self.problems: list[Problem] = []
        self.checked = 0
        self._gha = os.environ.get("GITHUB_ACTIONS") == "true"

    def add(self, path: Path, message: str, line: int | None = None) -> None:
        self.problems.append(Problem(path, line, message))

    def finish(self, unit: str = "items") -> int:
        root = repo_root()
        for p in self.problems:
            try:
                rel = p.path.relative_to(root).as_posix()
            except ValueError:
                rel = str(p.path)
            if self._gha:
                loc = f"file={rel}"
                if p.line:
                    loc += f",line={p.line}"
                print(f"::error {loc}::{p.message}")
            else:
                where = f"{rel}:{p.line}" if p.line else rel
                print(f"  {where}: {p.message}")

        if self.problems:
            print(f"\n{self.name}: FAILED - {len(self.problems)} problem(s) "
                  f"across {self.checked} {unit}")
            return 1
        print(f"{self.name}: OK - {self.checked} {unit} checked")
        return 0


def main_guard(fn):
    """Run a check function and exit with its return code."""
    try:
        sys.exit(fn())
    except KeyboardInterrupt:
        sys.exit(130)
