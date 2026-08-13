"""
Preflight check for the Tailwind Traders lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs.

Run it from the lab's starter code folder — Labfiles/A-build-and-extend-ai-agents/Python,
the folder you open in VS Code, where your virtual environment and .env live:

    python ../setup/check_env.py --task 3

This script uses only the Python standard library, so it works before you run
'pip install' and without the lab virtual environment active. Keep it that way:
it is the one script learners are most likely to run in a bare environment.

It never changes anything — it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (portal)  no .env needed — you build the agent in the portal
    Task 2  (code)    PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 3  (code)    PROJECT_ENDPOINT, AGENT_NAME   (the grounded portal agent)
    Task 4  (code)    PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 5  (code)    PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 6  (deploy)  PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
"""

import argparse
import os
from pathlib import Path

# Keep this script dependency-free. It is a *preflight* check, so it runs before
# 'pip install' and often on a bare system Python with no virtual environment
# active. Importing anything outside the standard library (python-dotenv
# included) would make it fail at exactly the moment it is most needed.


def read_env_file(env_path):
    """Parse a .env file into a dict, using only the standard library.

    Mirrors python-dotenv's dotenv_values() for the syntax these labs use:
    comments, blank lines, 'export KEY=value', single- and double-quoted values,
    inline comments after unquoted values, and bare keys (value None). Reads as
    utf-8-sig so a Notepad-saved .env carrying a UTF-8 BOM still resolves its
    first key. Returns an empty dict if the file cannot be read.
    """
    values = {}
    try:
        text = Path(env_path).read_text(encoding="utf-8-sig")
    except OSError:
        return values

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export ") or line.startswith("export\t"):
            line = line[len("export"):].lstrip()

        key, separator, value = line.partition("=")
        key = key.strip()
        if not key:
            continue
        if not separator:
            values[key] = None
            continue

        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            # Quoted: a '#' inside the quotes is data, not a comment.
            value = value[1:-1]
        else:
            for comment_marker in (" #", "\t#"):
                value = value.split(comment_marker, 1)[0]
            value = value.strip()
        values[key] = value

    return values

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: [],
    2: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    3: ["PROJECT_ENDPOINT", "AGENT_NAME"],
    4: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    5: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    6: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
}

# Placeholder text shipped in .env.example — present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your-project-endpoint",
    "your-model-deployment-name",
    "your-agent-name",
    "<your-project-endpoint>",
    "<your-model-deployment-name>",
    "<your-agent-name>",
}

# How to fix each key, shown only when it's missing.
FIX_HINTS = {
    "PROJECT_ENDPOINT": (
        "Copy your project endpoint from the Foundry portal (or the Foundry Toolkit "
        "VS Code extension: right-click the project deployment > Copy Project Endpoint), "
        "or run 'azd up' to provision one, then set PROJECT_ENDPOINT in .env."
    ),
    "MODEL_DEPLOYMENT_NAME": (
        "Set MODEL_DEPLOYMENT_NAME to the name of your deployed model "
        "(for example, gpt-4o). You can see it in the Foundry portal under your project."
    ),
    "AGENT_NAME": (
        "Task 3 needs the grounded portal agent from Task 1. Either complete Task 1 in "
        "the portal and set AGENT_NAME=tailwind-agent, or fast-forward past Task 1 by "
        "running, from the Python folder: python ../setup/bootstrap_agent.py"
    ),
}


def find_env_file():
    """Return the .env next to the lab's Python folder, wherever this is run from."""
    here = Path(__file__).resolve().parent
    candidates = [
        Path.cwd() / ".env",
        here.parent / "Python" / ".env",
        here.parent / ".env",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    # Default to the Python-folder location even if it doesn't exist yet.
    return here.parent / "Python" / ".env"


def load_values(env_path):
    """Merge real environment variables over .env file values (env wins)."""
    values = {}
    if env_path.exists():
        values.update({k: v for k, v in read_env_file(env_path).items() if v is not None})
    for key in ("PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME", "AGENT_NAME"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    return values


def is_set(values, key):
    """A key counts as set if it's present and not a leftover placeholder."""
    value = (values.get(key) or "").strip()
    return bool(value) and value not in PLACEHOLDERS


def main():
    parser = argparse.ArgumentParser(
        description="Check that your .env has what a given lab task needs."
    )
    parser.add_argument(
        "--task",
        type=int,
        choices=sorted(TASK_REQUIREMENTS),
        required=True,
        help="Which task you're about to start (1-6).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    if not required:
        print("Task 1 is completed entirely in the Foundry portal - no .env needed.")
        print("When you're ready for a code task, run this again with --task 2 (or higher).")
        return 0

    missing = [key for key in required if not is_set(values, key)]

    for key in required:
        mark = "OK " if is_set(values, key) else "MISSING"
        print(f"  [{mark}] {key}")

    if not missing:
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Set the following before starting this task:")
    for key in missing:
        print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
