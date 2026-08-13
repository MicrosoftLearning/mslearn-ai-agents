"""
Preflight check for the Tailwind Traders multi-agent lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs.

Run it from the lab's starter code folder —
Labfiles/C-build-multi-agent-solutions-with-agent-framework/Python, the folder you
open in VS Code, where your virtual environment and .env live:

    python ../setup/check_env.py --task 1

This script uses only the Python standard library, so it works before you run
'pip install' and without the lab virtual environment active. Keep it that way:
it is the one script learners are most likely to run in a bare environment.

It never changes anything — it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (code)   PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 2  (code)   PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 3  (code)   PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME,
                     SERVER_URL, TITLE_AGENT_PORT, OUTLINE_AGENT_PORT,
                     ROUTING_AGENT_PORT
    Task 4  (code)   PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
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
    1: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    2: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    3: [
        "PROJECT_ENDPOINT",
        "MODEL_DEPLOYMENT_NAME",
        "SERVER_URL",
        "TITLE_AGENT_PORT",
        "OUTLINE_AGENT_PORT",
        "ROUTING_AGENT_PORT",
    ],
    4: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
}

# Every key this lab might read, used when merging real environment variables.
ALL_KEYS = [
    "PROJECT_ENDPOINT",
    "MODEL_DEPLOYMENT_NAME",
    "SERVER_URL",
    "TITLE_AGENT_PORT",
    "OUTLINE_AGENT_PORT",
    "ROUTING_AGENT_PORT",
]

# Placeholder text shipped in .env.example — present but not yet filled in.
PLACEHOLDERS = {
    "",
    "your_project_endpoint_here",
    "your_model_deployment_name_here",
    "your-project-endpoint",
    "your-model-deployment-name",
    "<your-project-endpoint>",
    "<your-model-deployment-name>",
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
    "SERVER_URL": (
        "Task 3 runs the remote agents locally. Set SERVER_URL=localhost "
        "(this ships pre-filled in .env.example)."
    ),
    "TITLE_AGENT_PORT": (
        "Task 3 needs a port for the trip-title agent. Set TITLE_AGENT_PORT=10007 "
        "(this ships pre-filled in .env.example)."
    ),
    "OUTLINE_AGENT_PORT": (
        "Task 3 needs a port for the trip-itinerary agent. Set OUTLINE_AGENT_PORT=10008 "
        "(this ships pre-filled in .env.example)."
    ),
    "ROUTING_AGENT_PORT": (
        "Task 3 needs a port for the routing agent. Set ROUTING_AGENT_PORT=10009 "
        "(this ships pre-filled in .env.example)."
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
    for key in ALL_KEYS:
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
        help="Which task you're about to start (1-4).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

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
