"""
Preflight check for the Caldova observability lab.

Each task in this lab can be completed on its own. Before you start a task,
run this script to confirm your .env file has everything that task needs.

Run it from the lab's starter code folder —
Labfiles/D-observe-evaluate-and-secure-agents/Python, the folder you open in
VS Code, where your virtual environment and .env live:

    python ../setup/check_env.py --task 1

This script uses only the Python standard library, so it works before you run
'pip install' and without the lab virtual environment active. Keep it that way:
it is the one script learners are most likely to run in a bare environment.

It never changes anything — it only reads your .env and tells you what (if
anything) is missing, so you can fix it before running the task.

Tasks and what they need:

    Task 1  (core, code)      PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME
    Task 2  (core, code)      PROJECT_ENDPOINT, MODEL_DEPLOYMENT_NAME, AGENT_NAME
    Task 3  (optional, code)  PROJECT_ENDPOINT, AGENT_NAME

Task 1 also needs Application Insights connected to your Foundry project. That
is a connection on the project, not a value in .env, so this script cannot see
it — the page tells you how to connect it, and traced_agent.py fails with a
clear message if it is missing.
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

    Matches python-dotenv's dotenv_values() for every .env shape these labs can
    encounter: comments, blank lines, 'export KEY=value' (space or tab), single-
    and double-quoted values, escape sequences inside double quotes, inline
    comments, values quoted across several lines, and bare keys (value None).

    Matching python-dotenv matters because the lab apps load .env with
    python-dotenv. Whatever it returns is what the app actually sees, so the
    preflight has to agree with it rather than be a "better" parser -- a parser
    that is more forgiving than the runtime reports keys as present that the
    app cannot read.

    Returns an empty dict if the file cannot be read.
    """
    values, _ = _parse(env_path)
    return values


def find_env_problems(env_path):
    """Return a list of (summary, advice) for defects that always break the app.

    Only a BOM qualifies: it always corrupts the name of the first setting, so
    the file cannot work no matter which task the learner is starting. Other
    malformations are impact-dependent and come back from find_env_notes().
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
    return problems


def find_env_notes(env_path):
    """Return a list of (summary, advice) for malformed lines in the .env.

    These are reported but not automatically fatal. A stray quote only matters
    if it actually costs the learner a setting the task needs: an unterminated
    quote with nothing after it to swallow leaves a working file, and failing
    that would be its own false alarm. The caller decides, by checking whether
    the keys the task needs came through.

    Detection reads the file directly rather than inferring from parser output,
    because python-dotenv reports malformed statements to stderr and simply
    omits them from its result -- the app just sees a setting vanish with no
    indication of why.
    """
    notes = []
    _, defects = _parse(env_path)
    for kind, number, text in defects:
        if kind == "unterminated":
            notes.append((
                f"unterminated quote on line {number} of .env",
                f"That line is:  {text}\n"
                "    It opens a quote that is never closed, so the lab apps drop\n"
                "    that setting entirely. Close the quote, or remove both quotes\n"
                "    -- values in .env do not need them.",
            ))
        elif kind == "swallowed":
            notes.append((
                f"quote opened on line {number} of .env is closed much later",
                f"That line is:  {text}\n"
                "    Everything up to the next quote further down the file becomes\n"
                "    part of this one value, so the settings in between are lost\n"
                "    even though they look correct. Close the quote on this line,\n"
                "    or remove both quotes.",
            ))
        elif kind == "trailing":
            notes.append((
                f"unexpected text after the quoted value on line {number} of .env",
                f"That line is:  {text}\n"
                "    python-dotenv cannot parse the line, so the lab apps drop that\n"
                "    setting. Keep the value inside one pair of quotes, and put\n"
                "    nothing after the closing quote except a # comment.",
            ))
    return notes


def _has_bom(env_path):
    """True if the file starts with a UTF-8 BOM."""
    try:
        with open(env_path, "rb") as handle:
            return handle.read(3) == b"\xef\xbb\xbf"
    except OSError:
        return False


def _looks_like_assignment(line):
    """True for a line shaped like KEY=..., used to spot swallowed settings."""
    head = line.strip().partition("=")
    if not head[1]:
        return False
    name = head[0].strip()
    if name.startswith("export "):
        name = name[len("export "):].strip()
    return bool(name) and name.replace("_", "").isalnum()


def _parse(env_path):
    """Return (values, defects).

    defects is a list of (kind, line_number, line_text) where kind is one of
    "unterminated", "swallowed" or "trailing".

    Quoted values are resolved with a lookahead that only advances when a
    closing quote is actually found, which is what python-dotenv does: a quote
    closed on a later line is a legitimate multi-line value, while a quote that
    is never closed makes python-dotenv discard that statement and resume at
    the next line.
    """
    values = {}
    defects = []
    try:
        # utf-8-sig strips a BOM so the remaining keys are reported accurately.
        # The BOM itself is surfaced separately by find_env_problems().
        text = Path(env_path).read_text(encoding="utf-8-sig")
    except OSError:
        return values, defects

    lines = text.splitlines()
    index = 0
    while index < len(lines):
        number = index + 1
        line = lines[index].strip()
        index += 1

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
        if value[:1] not in ("'", '"'):
            for comment_marker in (" #", "\t#"):
                value = value.split(comment_marker, 1)[0]
            values[key] = value.strip()
            continue

        quote = value[0]
        # Join the rest of the file so a value may close on a later line.
        rest = "\n".join([value] + lines[index:])
        inner, closed, end, usable = _scan_for_close(rest, quote)
        if not closed:
            defects.append(("unterminated", number, line))
            continue

        consumed = rest.count("\n", 0, end)
        if not usable:
            # python-dotenv cannot parse the statement and drops it. If the
            # quote also spanned lines, report it as a swallow: the settings it
            # ate are the part the learner can actually see and act on.
            defects.append(("swallowed" if consumed else "trailing", number, line))
            index += consumed
            continue

        if consumed:
            swallowed = lines[index:index + consumed]
            if any(_looks_like_assignment(item) for item in swallowed):
                defects.append(("swallowed", number, line))
            index += consumed

        values[key] = inner

    return values, defects


# Escape sequences python-dotenv decodes, per quote character. Double quotes
# take the full set; single quotes decode only the delimiter and a literal
# backslash, so '\n' inside single quotes stays as a backslash and an n.
# Anything not listed keeps its backslash.
_ESCAPES = {
    '"': {
        "a": "\a",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "v": "\v",
        '"': '"',
        "'": "'",
        "\\": "\\",
    },
    "'": {"'": "'", "\\": "\\"},
}


def _scan_for_close(text, quote):
    """Find where a quoted value ends, the way python-dotenv does.

    Returns (contents, closed, end_index, usable). usable is False when
    python-dotenv could not parse the statement and dropped it, in which case
    end_index still says where parsing resumes.

    Two passes, matching python-dotenv:

    1. Escape-aware, using the escape set for whichever character opened the
       value (see _ESCAPES). A backslash-escaped quote is skipped rather than
       treated as the close. If this closes with nothing but whitespace or a
       comment after it, the value is good.
    2. Raw, only if the first pass finds no close anywhere. Nothing is exempt
       here: a matching character inside a comment, inside a differently quoted
       value, or in an unquoted value all close the run.

    A close found by pass 2, or a pass-1 close followed by text python-dotenv
    cannot parse, means the statement is unparseable: its key is dropped and
    parsing resumes after the close that was found.
    """
    contents, closed, end = _read_quoted(text, quote, escape_aware=True)
    if closed:
        tail = text[end:].split("\n", 1)[0].strip()
        if not tail or tail.startswith("#"):
            return contents, True, end, True
        # Closed, but python-dotenv cannot parse what follows, so it drops the
        # statement. end still says where parsing resumes.
        return contents, True, end, False

    # Recovery. python-dotenv's value pattern failed to match, and it then
    # resynchronises on the LAST occurrence of the quote character rather than
    # the first, so everything up to that point is lost. Measured: keys after
    # that final occurrence survive, and if there are none, nothing does.
    last = text.rfind(quote, 1)
    if last == -1:
        return "", False, len(text), False
    return text[1:last], True, last + 1, False


def _read_quoted(text, quote, escape_aware):
    """Return (contents, closed, end_index) for text starting with a quote.

    end_index is the position just past the closing quote. A '#' inside the
    quotes is data, not a comment.

    When escape_aware, backslash escapes are expanded in a single pass, so an
    escaped quote does not end the run and a literal backslash is never
    re-interpreted. The caller decides when that applies: parsing a value
    honours escapes in double quotes only, while recovering from an unclosed
    quote honours them for either character.
    """
    chars = []
    index = 1
    while index < len(text):
        char = text[index]
        if escape_aware and char == "\\" and index + 1 < len(text):
            following = text[index + 1]
            decoded = _ESCAPES.get(quote, {})
            chars.append(decoded.get(following, "\\" + following))
            index += 2
            continue
        if char == quote:
            return "".join(chars), True, index + 1
        chars.append(char)
        index += 1
    return "".join(chars), False, index

# Which .env keys each task needs to run on its own.
TASK_REQUIREMENTS = {
    1: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME"],
    2: ["PROJECT_ENDPOINT", "MODEL_DEPLOYMENT_NAME", "AGENT_NAME"],
    3: ["PROJECT_ENDPOINT", "AGENT_NAME"],
}

def looks_like_placeholder(value):
    """True if the value is still example text rather than a real setting.

    Matched by shape rather than an exact list. The shipped .env.example files
    have used both 'your-project-endpoint' and 'your_project_endpoint_here',
    and an exact list silently rots the moment one of them changes -- which is
    exactly what happened: a learner could copy .env.example verbatim, change
    nothing, and be told they were ready to start.

    Anything empty, wrapped in angle brackets, or whose first word is "your"
    counts as unfilled. Real defaults these labs ship (caldova-agent,
    caldova-knowledge-agent, localhost, port numbers) do not match.

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
        "Tasks 2 and 3 evaluate a grounded agent. Either reuse the knowledge agent "
        "from Lab B and set AGENT_NAME to its name, or create one here by running, "
        "from the Python folder: python ../setup/bootstrap_agent.py"
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



def report_items(heading, items):
    """Print each .env defect and how to fix it."""
    print()
    print(heading)
    for summary, advice in items:
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
        help="Which task you're about to start (1-3).",
    )
    args = parser.parse_args()

    env_path = find_env_file()
    values = load_values(env_path)
    required = TASK_REQUIREMENTS[args.task]
    problems = find_env_problems(env_path) if env_path.exists() else []
    notes = find_env_notes(env_path) if env_path.exists() else []

    print(f"Checking readiness for Task {args.task}")
    print(f"Reading: {env_path}{'' if env_path.exists() else '  (not found yet)'}")
    print()

    # A BOM always corrupts the first setting's name, so the file cannot work
    # whatever the task needs. Report it on its own: listing keys as OK/MISSING
    # alongside it would either bless a broken file or point at the wrong thing.
    if problems:
        for summary, _ in problems:
            print(f"  [PROBLEM] {summary}")
        report_items("Fix your .env before starting this task:", problems)
        return 1

    missing = [key for key in required if not is_set(values, key)]

    for key in required:
        mark = "OK " if is_set(values, key) else "MISSING"
        print(f"  [{mark}] {key}")
    for summary, _ in notes:
        print(f"  [NOTE] {summary}")

    # A malformed line only matters if it actually cost this task a setting.
    # A stray quote with nothing after it to swallow leaves a working file, and
    # failing that would be a false alarm in the other direction.
    if not missing:
        if notes:
            report_items(
                "One line in your .env is malformed, but nothing this task "
                "needs is affected:",
                notes,
            )
        print()
        print(f"You're ready to start Task {args.task}.")
        return 0

    print()
    print("Set the following before starting this task:")
    for key in missing:
        print(f"\n  {key}\n    {FIX_HINTS.get(key, 'Add this key to your .env file.')}")
    if notes:
        report_items("This may be why -- your .env has a malformed line:", notes)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
