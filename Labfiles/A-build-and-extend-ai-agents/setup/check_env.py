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

    Matches python-dotenv's dotenv_values() for every well-formed .env these
    labs use: comments, blank lines, 'export KEY=value' (space or tab), single-
    and double-quoted values, escape sequences inside double quotes, inline
    comments after a value, and bare keys (value None). Returns an empty dict
    if the file cannot be read.

    Matching python-dotenv matters because the lab apps load .env with
    python-dotenv: whatever it returns is what the app actually sees, so the
    preflight has to agree with it rather than be a "better" parser.

    Malformed files are handled by find_env_problems() instead -- see the note
    there for why this function does not try to imitate python-dotenv's
    behaviour on broken input.
    """
    values, _ = _parse(env_path)
    return values


def find_env_problems(env_path):
    """Return a list of (summary, advice) for defects that break the lab apps.

    Some .env defects do not make a key "missing" so much as make the file
    unusable in ways the learner cannot see. For those we refuse to give a
    per-key verdict at all: reporting "[OK] PROJECT_ENDPOINT" for a file the
    app cannot read would be a false positive, and reporting unrelated keys as
    MISSING would send the learner hunting the wrong problem. Instead we name
    the defect, explain the cause, and exit non-zero.

    Detected:

    * UTF-8 BOM. python-dotenv does not strip it, so it becomes part of the
      first setting's NAME and the app's os.getenv() for that setting returns
      None even though the file looks correct.
    * Unterminated quote. python-dotenv treats the opening quote as the start
      of a multi-line value. What that costs depends on the rest of the file:
      with no later quote it drops just that entry, but if a quote appears
      further down it swallows everything in between, silently wiping settings
      that are themselves written correctly.
    """
    problems = []
    if _has_bom(env_path):
        problems.append((
            ".env starts with a UTF-8 BOM",
            "Your .env was saved as 'UTF-8 with BOM' (Notepad does this by\n"
            "    default). The BOM becomes part of the first setting's name, so the\n"
            "    lab apps read that setting as empty even though the file looks\n"
            "    correct. Re-save as plain UTF-8: in VS Code click the encoding\n"
            "    indicator in the status bar, choose 'Save with Encoding', then\n"
            "    'UTF-8' (not 'UTF-8 with BOM').",
        ))

    _, open_quote_line = _parse(env_path)
    if open_quote_line is not None:
        number, text = open_quote_line
        problems.append((
            f"unterminated quote on line {number} of .env",
            f"That line is:  {text}\n"
            "    It opens a quote that is never closed. The lab apps then treat\n"
            "    everything after it as part of that one value, which can silently\n"
            "    wipe out settings further down the file. Close the quote, or\n"
            "    remove both quotes -- values in .env do not need them.",
        ))
    return problems


def _has_bom(env_path):
    """True if the file starts with a UTF-8 BOM."""
    try:
        with open(env_path, "rb") as handle:
            return handle.read(3) == b"\xef\xbb\xbf"
    except OSError:
        return False


def _parse(env_path):
    """Return (values, first_unterminated_quote) for a .env file.

    first_unterminated_quote is None, or (line_number, stripped_line).
    """
    values = {}
    bad_quote = None
    try:
        # utf-8-sig strips a BOM so the remaining keys are reported accurately.
        # The BOM itself is surfaced separately by find_env_problems().
        text = Path(env_path).read_text(encoding="utf-8-sig")
    except OSError:
        return values, bad_quote

    for number, raw_line in enumerate(text.splitlines(), start=1):
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
        if value[:1] in ("'", '"'):
            inner, closed = _read_quoted(value, value[0])
            if not closed:
                if bad_quote is None:
                    bad_quote = (number, line)
                continue
            # Anything after the closing quote (such as ' # comment') is dropped.
            value = inner
        else:
            for comment_marker in (" #", "\t#"):
                value = value.split(comment_marker, 1)[0]
            value = value.strip()
        values[key] = value

    return values, bad_quote


# Escape sequences python-dotenv expands inside double-quoted values.
_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", "'": "'", '"': '"'}


def _read_quoted(value, quote):
    """Return (contents, closed) for a value that starts with a quote character.

    A '#' inside the quotes is data, not a comment. Inside double quotes,
    backslash escapes are expanded in a single pass, so an escaped quote does
    not end the value and a literal backslash is never re-interpreted.
    """
    chars = []
    index = 1
    while index < len(value):
        char = value[index]
        if char == "\\" and quote == '"' and index + 1 < len(value):
            following = value[index + 1]
            chars.append(_ESCAPES.get(following, "\\" + following))
            index += 2
            continue
        if char == quote:
            return "".join(chars), True
        chars.append(char)
        index += 1
    return "".join(chars), False

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: [],
    2: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    3: ["PROJECT_ENDPOINT", "AGENT_NAME"],
    4: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    5: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    6: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
}

def looks_like_placeholder(value):
    """True if the value is still example text rather than a real setting.

    Matched by shape rather than an exact list. The shipped .env.example files
    have used both 'your-project-endpoint' and 'your_project_endpoint_here',
    and an exact list silently rots the moment one of them changes -- which is
    exactly what happened: a learner could copy .env.example verbatim, change
    nothing, and be told they were ready to start.

    Anything empty, wrapped in angle brackets, or whose first word is "your"
    counts as unfilled. Real defaults these labs ship (tailwind-agent,
    tailwind-knowledge-agent, localhost, port numbers) do not match.

    This deliberately errs toward "not filled in": a real value beginning with
    the word "your" would be flagged, but none of these keys takes one (they
    hold a URL, a model deployment name, a slug or a port). Being told to
    double-check a key you did set is recoverable; being told you are ready
    when you are not is the failure this whole script exists to prevent.
    """
    text = value.strip()
    if not text:
        return True
    if text.startswith("<") and text.endswith(">"):
        return True
    words = text.replace("-", " ").replace("_", " ").lower().split()
    return bool(words) and words[0] == "your"

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
    return not looks_like_placeholder(values.get(key) or "")



def report_problems(problems):
    """Print each .env defect and how to fix it."""
    print()
    print("Fix your .env before starting this task:")
    for summary, advice in problems:
        print(f"\n  {summary}\n    {advice}")

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
    problems = find_env_problems(env_path) if env_path.exists() else []

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    if not required:
        print("Task 1 is completed entirely in the Foundry portal - no .env needed.")
        print("When you're ready for a code task, run this again with --task 2 (or higher).")
        if problems:
            for summary, _ in problems:
                print(f"\n  [PROBLEM] {summary}")
            report_problems(problems)
            return 1
        return 0

    # A malformed .env is reported on its own. Listing keys as OK/MISSING
    # alongside it would either claim a broken file is fine, or point the
    # learner at keys that are only "missing" because of the real defect.
    if problems:
        for summary, _ in problems:
            print(f"  [PROBLEM] {summary}")
        report_problems(problems)
        return 1

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
