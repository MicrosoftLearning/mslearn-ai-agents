#!/usr/bin/env python3
"""Copy the shared lab infrastructure into each lab that uses it.

Every consolidated lab ships the same azd template, Bicep and post-provision
scripts. Keeping physical copies is deliberate: a learner downloads one lab
folder and everything it needs is inside it. The risk is that the copies drift,
and nothing tells you when one is missed.

So the copies stay, and this keeps them honest. Edit the canonical file under
Labfiles/_shared/, run this, and commit both.

    python Labfiles/_shared/sync.py            # regenerate every consumer
    python Labfiles/_shared/sync.py --check    # fail if any copy has drifted
    python Labfiles/_shared/sync.py --lab A-build-and-extend-ai-agents

Only files that are identical (or identical apart from a couple of tokens) are
managed here. check_env.py, bootstrap_agent.py and requirements.txt are
genuinely lab-specific and are left alone.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

import yaml

SHARED = Path(__file__).resolve().parent
LABFILES = SHARED.parent

BANNER_PREFIX = {
    ".bicep": "// ",
    ".yaml": "# ",
    ".ps1": "# ",
    ".sh": "# ",
}
BANNER_TEXT = [
    "GENERATED FROM Labfiles/_shared/ - DO NOT EDIT THIS COPY.",
    "Edit the file under Labfiles/_shared/, then run:",
    "    python Labfiles/_shared/sync.py",
]

# source (relative to _shared)  ->  destination (relative to the lab folder)
FILES = {
    "infra/main.bicep": "infra/main.bicep",
    "infra/resources.bicep": "infra/resources.bicep",
    "infra/main.parameters.json": "infra/main.parameters.json",
    "setup/write_env.ps1": "setup/write_env.ps1",
    "setup/write_env.sh": "setup/write_env.sh",
    "azure.yaml": "azure.yaml",
}


def banner_for(path: Path) -> str:
    """Comment banner for a file type, or '' where comments aren't allowed."""
    prefix = BANNER_PREFIX.get(path.suffix)
    if not prefix:
        return ""  # JSON has no comment syntax
    return "".join(f"{prefix}{line}\n" for line in BANNER_TEXT) + "\n"


def render(source: Path, dest_name: Path, lab_folder: str, cfg: dict) -> str:
    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    text = (
        text.replace("{{LAB_FOLDER}}", lab_folder)
        .replace("{{AZD_NAME}}", cfg["azd_name"])
        .replace("{{LAB_DESCRIPTION}}", cfg["description"])
        .replace("{{LAB_HINT}}", " ".join(cfg["hint"].split()))
    )
    if "{{" in text:
        raise SystemExit(f"unresolved token in {source}: check manifest.yml")

    body = banner_for(dest_name) + text
    # A shebang has to stay on line 1.
    if text.startswith("#!"):
        first, _, rest = text.partition("\n")
        body = first + "\n" + banner_for(dest_name) + rest
    return body


def to_bytes(text: str, dest_name: Path) -> bytes:
    """Encode canonical LF text for disk.

    .gitattributes checks Windows scripts out as CRLF, so they are written that
    way. Comparison always happens on the LF form, so this never shows as drift.
    """
    if dest_name.suffix in {".ps1", ".cmd", ".bat"}:
        text = text.replace("\n", "\r\n")
    return text.encode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report drift, change nothing")
    ap.add_argument("--lab", help="limit to one lab folder name")
    args = ap.parse_args()

    manifest = yaml.safe_load((SHARED / "manifest.yml").read_text(encoding="utf-8"))
    labs = manifest["labs"]
    if args.lab:
        if args.lab not in labs:
            print(f"{args.lab} is not in manifest.yml")
            return 2
        labs = {args.lab: labs[args.lab]}

    drifted, written = [], []

    for lab_folder, cfg in labs.items():
        lab_dir = LABFILES / lab_folder
        if not lab_dir.is_dir():
            print(f"missing lab folder: {lab_folder}")
            return 2

        for src_rel, dest_rel in FILES.items():
            source = SHARED / src_rel
            dest = lab_dir / dest_rel
            expected = render(source, Path(dest_rel), lab_folder, cfg)

            current = (
                dest.read_text(encoding="utf-8").replace("\r\n", "\n")
                if dest.exists()
                else None
            )
            if current == expected:
                continue

            rel = dest.relative_to(LABFILES.parent).as_posix()
            if args.check:
                drifted.append(rel)
                diff = difflib.unified_diff(
                    (current or "").splitlines(keepends=True),
                    expected.splitlines(keepends=True),
                    fromfile=f"{rel} (in repo)",
                    tofile=f"{rel} (expected)",
                    n=1,
                )
                sys.stdout.writelines(diff)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(to_bytes(expected, Path(dest_rel)))
                written.append(rel)

    if args.check:
        if drifted:
            print(f"\nshared infrastructure: DRIFTED - {len(drifted)} file(s)")
            print("Run: python Labfiles/_shared/sync.py")
            return 1
        print(f"shared infrastructure: OK - {len(labs)} lab(s) in sync")
        return 0

    print(f"synced {len(labs)} lab(s); {len(written)} file(s) updated")
    for w in written:
        print("  ", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
