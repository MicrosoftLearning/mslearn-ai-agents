#!/usr/bin/env python3
"""Check that tracked text files honour the .gitattributes line-ending policy.

The repo pins LF for text files so branches stop diverging on line endings.
Tooling that writes files with platform newlines silently undoes that - Python's
Path.write_text() on Windows is a common culprit - and the result is a whole-file
diff on a file nobody meaningfully changed.

This inspects the git index rather than the working tree, because that is what
the policy actually governs.
"""

import subprocess

from common import Reporter, main_guard, repo_root

# Windows scripts are intentionally CRLF, matching .gitattributes.
CRLF_ALLOWED_SUFFIXES = (".ps1", ".cmd", ".bat")


def check() -> int:
    r = Reporter("line endings")
    root = repo_root()

    out = subprocess.run(
        ["git", "ls-files", "--eol"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    for raw in out.splitlines():
        # Format: "i/lf    w/lf    attr/text=auto eol=lf   path"
        parts = raw.split("\t")
        if len(parts) < 2:
            continue
        flags, path = parts[0], parts[-1].strip()

        if "i/none" in flags or "i/-text" in flags:
            continue  # binary

        r.checked += 1
        if "i/crlf" not in flags and "i/mixed" not in flags:
            continue
        if path.endswith(CRLF_ALLOWED_SUFFIXES):
            continue

        kind = "mixed" if "i/mixed" in flags else "CRLF"
        r.add(
            root / path,
            f"{kind} line endings in the git index; expected LF. "
            f"Run: git add --renormalize {path}",
        )

    return r.finish("tracked text files")


if __name__ == "__main__":
    main_guard(check)
