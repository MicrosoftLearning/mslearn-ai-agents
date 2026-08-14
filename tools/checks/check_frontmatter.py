#!/usr/bin/env python3
"""Check that every lab page has valid, minimally complete frontmatter.

Catches the failure mode where a YAML typo makes a page unparseable and the
site build breaks - most commonly an unescaped apostrophe inside a
single-quoted scalar, e.g.  verify: 'you don't have access'

This deliberately validates only fields that exist across all lab pages today.
Strict schema validation (type/section/difficulty/order) lands once the
consolidated labs carry that metadata.
"""

import sys

import yaml

from common import Reporter, lab_pages, main_guard, split_frontmatter

REQUIRED = ("title",)


def check() -> int:
    r = Reporter("frontmatter")

    for path in lab_pages():
        r.checked += 1
        text = path.read_text(encoding="utf-8")
        fm, _ = split_frontmatter(text)

        if fm is None:
            r.add(path, "no YAML frontmatter block found", 1)
            continue

        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as e:
            mark = getattr(e, "problem_mark", None)
            line = (mark.line + 2) if mark else 1  # +1 for the opening ---, +1 for 0-index
            problem = getattr(e, "problem", str(e))
            r.add(path, f"invalid YAML frontmatter: {problem}", line)
            continue

        if not isinstance(data, dict):
            r.add(path, "frontmatter is not a mapping", 1)
            continue

        lab = data.get("lab")
        if not isinstance(lab, dict):
            r.add(path, "missing 'lab:' mapping in frontmatter", 1)
            continue

        for key in REQUIRED:
            if not lab.get(key):
                r.add(path, f"frontmatter is missing lab.{key}", 1)

    return r.finish("pages")


if __name__ == "__main__":
    main_guard(check)
