#!/usr/bin/env python3
"""Tier 1: verify the lab code still matches the SDKs it is pinned against.

This installs a lab's pinned requirements and checks that every module and
symbol the lab imports still resolves - both in the Python files the lab ships
and in the code blocks the instructions tell learners to paste.

It needs no Azure resources, no credentials and no spend, so it can run nightly.

That matters because the breakages this repo actually hits are import- and
signature-level. Recent examples from the history:

  - "Fix Exercise 3: Update FastMCP import to standalone package"
  - "Update labs 02 and 03 to azure-ai-projects==2.0.0b4"
  - "Revert agent-framework bump on legacy labs 07/08"

Every one would have been caught here before a learner hit it.

The import contract is derived from the content rather than hand-maintained, so
it cannot drift. Only keyword arguments are pinned explicitly, below.

Usage:
    python check_sdk_contract.py --list
    python check_sdk_contract.py --lab 07-agent-framework
"""

from __future__ import annotations

import argparse
import ast
import importlib
import importlib.util
import inspect
import re
import sys
import textwrap
from pathlib import Path

from common import Reporter, main_guard, repo_root

FENCE = re.compile(r"(?ms)^[ \t]*```python[ \t]*\r?\n(.*?)^[ \t]*```")

# Keyword arguments the instructions pass explicitly. Unlike imports these
# cannot be derived reliably, so they are pinned here: if an SDK renames one,
# the labs break silently and this is what catches it.
KWARG_CONTRACTS = [
    ("azure.ai.projects", "AIProjectClient", ["endpoint", "credential"]),
]

SKIP_DIRS = {"labenv", "venv", "__pycache__", "node_modules"}


def lab_dirs() -> list[Path]:
    root = repo_root() / "Labfiles"
    return sorted(p for p in root.iterdir() if p.is_dir() and (p / "Python").is_dir())


def lab_prefix(name: str) -> str:
    """'08-agent-orchestration' -> '08';  'A-build-and-extend' -> 'A'."""
    return name.split("-", 1)[0]


def pages_for(lab: Path) -> list[Path]:
    """Instruction pages belonging to a lab, matched on filename prefix.

    Page and folder names don't always match in full - '08-agent-framework-
    multi-agents.md' documents 'Labfiles/08-agent-orchestration' - but the
    leading token is stable.
    """
    prefix = lab_prefix(lab.name)
    pages = []
    for d in ("Instructions/Exercises", "Instructions/Consolidated"):
        folder = repo_root() / d
        if not folder.is_dir():
            continue
        for p in sorted(folder.glob("*.md")):
            if lab_prefix(p.stem) == prefix:
                pages.append(p)
    return pages


def imports_in(tree: ast.AST):
    """Yield (module, symbol_or_None, lineno) for absolute imports."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                yield a.name, None, node.lineno
        elif isinstance(node, ast.ImportFrom):
            if node.level or not node.module:
                continue  # relative import, resolved inside the lab
            for a in node.names:
                yield node.module, a.name, node.lineno


# Starter files are intentionally not valid Python: placeholders sit where the
# learner adds a `with` block or a function body, so the code below them is
# pre-indented. Only Solution/ files are required to parse.


def collect_from_lab(lab: Path):
    """Yield (source, module, symbol, line); module is None for a syntax error."""
    for base in ("Python", "Solution/Python"):
        src = lab / base
        if not src.is_dir():
            continue
        is_solution = base.startswith("Solution")
        for py in sorted(src.rglob("*.py")):
            if any(part in SKIP_DIRS for part in py.parts):
                continue
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError as e:
                if not is_solution:
                    # Expected: the learner fills in the blanks. Imports for
                    # these files are covered by the instruction code blocks.
                    continue
                yield py, None, f"is not valid Python: {e.msg}", e.lineno
                continue
            for module, symbol, line in imports_in(tree):
                yield py, module, symbol, line


def collect_from_pages(lab: Path):
    """Yield (page, module, symbol, line) for imports inside code blocks."""
    for page in pages_for(lab):
        text = page.read_text(encoding="utf-8")
        for m in FENCE.finditer(text):
            code = textwrap.dedent(m.group(1))
            if "import" not in code:
                continue
            try:
                tree = ast.parse(code)
            except SyntaxError:
                continue  # snippet completeness is check_code_blocks.py's job
            fence_line = text[: m.start()].count("\n") + 1
            for module, symbol, line in imports_in(tree):
                yield page, module, symbol, fence_line + line


def check_kwargs(r: Reporter) -> None:
    for module_name, symbol, kwargs in KWARG_CONTRACTS:
        if importlib.util.find_spec(module_name) is None:
            continue
        try:
            module = importlib.import_module(module_name)
        except Exception:  # noqa: BLE001
            continue
        obj = getattr(module, symbol, None)
        if obj is None:
            continue
        try:
            sig = inspect.signature(obj)
        except (TypeError, ValueError):
            continue
        if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
            continue
        for kw in kwargs:
            r.checked += 1
            if kw not in sig.parameters:
                r.add(
                    repo_root(),
                    f"{module_name}.{symbol} no longer accepts '{kw}' "
                    f"(the lab instructions pass it)",
                )


def check() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lab", help="lab folder name under Labfiles/")
    ap.add_argument("--list", action="store_true", help="list labs and exit")
    args = ap.parse_args()

    if args.list:
        for d in lab_dirs():
            print(d.name)
        return 0
    if not args.lab:
        ap.error("--lab is required (or use --list)")

    lab = repo_root() / "Labfiles" / args.lab
    if not lab.is_dir():
        print(f"no such lab: {args.lab}")
        return 2

    r = Reporter(f"sdk contract [{args.lab}]")

    local_names = {"setup"}
    for base in ("Python", "Solution/Python"):
        src = lab / base
        if src.is_dir():
            for py in src.rglob("*.py"):
                local_names.add(py.stem)
                local_names.add(py.parent.name)

    records = []
    for source, module, symbol, line in collect_from_lab(lab):
        if module is None:  # syntax error; `symbol` holds the message
            r.checked += 1
            r.add(source, symbol, line)
            continue
        records.append((source, module, symbol, line))
    records.extend(collect_from_pages(lab))

    missing: set[tuple[Path, str]] = set()
    seen: set[tuple[str, str]] = set()

    for source, module, symbol, line in records:
        root_pkg = module.split(".")[0]
        if root_pkg in local_names or root_pkg in sys.stdlib_module_names:
            continue

        if (source, module) in missing:
            continue
        try:
            found = importlib.util.find_spec(module) is not None
        except (ImportError, ValueError):
            found = False
        if not found:
            r.checked += 1
            missing.add((source, module))
            r.add(source, f"import target not found: {module}", line)
            continue

        if symbol is None or symbol == "*":
            continue
        if (module, symbol) in seen:
            continue
        seen.add((module, symbol))

        r.checked += 1
        try:
            mod = importlib.import_module(module)
        except Exception as e:  # noqa: BLE001
            r.add(source, f"failed to import {module}: {type(e).__name__}: {e}", line)
            continue
        try:
            present = hasattr(mod, symbol)
        except Exception as e:  # noqa: BLE001
            # Lazy __getattr__ shims (agent_framework does this) raise
            # ModuleNotFoundError rather than AttributeError for an optional
            # sub-package that isn't installed.
            r.add(source, f"{module}.{symbol} unavailable: {type(e).__name__}: {e}", line)
            continue
        if not present:
            r.add(source, f"{module} no longer exports '{symbol}'", line)

    check_kwargs(r)
    return r.finish("imports")


if __name__ == "__main__":
    main_guard(check)
