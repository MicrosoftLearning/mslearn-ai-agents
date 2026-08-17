# Lab content checks

Automated checks that catch problems in the lab content before a learner hits
them. They are deliberately cheap: **no Azure resources, no credentials, and no
spend**, so they can run on every pull request.

## Running them locally

```
pip install -r tools/checks/requirements.txt
python tools/checks/check_frontmatter.py
python tools/checks/check_code_blocks.py
python tools/checks/check_links.py
python tools/checks/check_line_endings.py
```

Each script exits non-zero when it finds a problem and prints the file and line.
In GitHub Actions the same output becomes an inline annotation on the pull
request diff.

## Tier 0 — content checks (every pull request, and every push to `main`)

| Check | What it catches |
| --- | --- |
| `check_frontmatter.py` | YAML that won't parse, which breaks the site build. The usual cause is an unescaped apostrophe inside a single-quoted value, such as `verify: 'you don't have access'`. |
| `check_code_blocks.py` | A ```` ```python ```` block that isn't valid Python. Learners paste these straight into a file, so a bad indent breaks the lab. |
| `check_links.py` | A link to a page that was renamed or moved, or a screenshot that no longer exists. |
| `check_line_endings.py` | Text files drifting back to CRLF in the index, against the `.gitattributes` policy. |
| `generate_lab_blocks.py --check` | A generated block in a lab page — the task table, or a gated-access notice — no longer matching the frontmatter it is built from. |
| `Labfiles/_shared/sync.py --check` | A lab's copy of the shared azd template, Bicep or post-provision scripts drifting from the canonical version. See [`Labfiles/_shared/README.md`](../../Labfiles/_shared/README.md). |

### Why the lab pages contain generated markdown rather than Liquid

The lab instruction pages are read directly by platforms that never run Liquid.
GitHub's own markdown renderer is one: a `{% include %}` in a `.md` file shows
up verbatim where the content should be. Confirmed by rendering one through
GitHub's markdown API, which returns
`<p>{% include lab-tasks-table.html lab='A' %}</p>`.

So those pages stay plain markdown, and `tools/generate_lab_blocks.py` writes
the generated parts between HTML comment markers — invisible in every renderer:

```
<!-- BEGIN GENERATED: task-table - do not edit by hand; ... -->
| Section | Task | Level | Time |
...
<!-- END GENERATED: task-table -->
```

Frontmatter stays the single source of truth, the output is real markdown that
works everywhere, and `--check` makes drift a build failure. A lab page that is
missing its markers is an error, so a new lab cannot silently ship without its
table.

The web-only pages — `workshop.md`, `explore.md`, `labs.json` — still use Liquid
directly. They are never consumed as raw markdown, so there is nothing to work
around.

### Why the code block check normalizes first

The blocks are snippets, not programs, so parsing them as-is is useless — 134 of
148 blocks in this repo would report a false positive. The check therefore:

1. **Dedents** the block, because snippets are indented to sit inside a function
   body.
2. **Closes a trailing open block** if parsing failed *only* because a `with` or
   `def` has no body — the lab adds that body in a later step.

A genuine syntax error — a typo, an unbalanced bracket, or a bad indent *within*
the snippet — still fails. That is the class of bug behind the `fix fence
indentation` and `fix code sample indentation` fixes on `main`.

## Tier 1 — SDK contract (nightly)

`check_sdk_contract.py` installs each lab's pinned requirements, then checks that
every module and symbol the lab imports still resolves — both in the Python
files the lab ships **and in the code blocks the instructions tell learners to
paste**.

It runs nightly, and on any pull request that touches a `requirements.txt`, the
check itself, or its workflow — the changes most likely to break it. It is
path-filtered because it installs dependencies across a matrix of every lab,
which is too slow to run on unrelated pull requests.

This targets the breakages this repo actually hits, which are import- and
signature-level:

- *Fix Exercise 3: Update FastMCP import to standalone package*
- *Update labs 02 and 03 to `azure-ai-projects==2.0.0b4`*
- *Revert agent-framework bump on legacy labs 07/08*

Each would have been caught here, without any Azure resources, before reaching a
learner.

It runs twice per lab. **Pinned** uses the versions in `requirements.txt`; a
failure means something was yanked or a transitive dependency broke. **Latest**
strips the pins; a failure there is early warning for the next version bump and
does not fail the job.

Because these labs are maintained asynchronously, a scheduled failure opens a
GitHub issue rather than relying on someone noticing a red badge.

### The import contract maintains itself

There is no hand-written list of expected symbols. The contract is derived from
the content, so it cannot drift: add an import to a lab or an instruction code
block and it is checked automatically.

Only **keyword arguments** are pinned by hand, in `KWARG_CONTRACTS`, because
they can't be derived reliably. If you change a code block to pass a new
argument, add it there so a future SDK rename fails loudly instead of silently
breaking the lab.

Starter files are expected to be incomplete — a `def` whose body the learner
fills in later is a syntax error by design — so a parse failure with that
signature is ignored outside `Solution/`.

## Not yet covered

These need groundwork that doesn't exist yet:

| Check | Blocked on |
| --- | --- |
| Strict frontmatter schema (`type`, `section`, `difficulty`, `order`) | The consolidated labs carrying that metadata. |
| Generated task tables match frontmatter | The same metadata, plus the table include. |
| Instructions match the `Solution/` code | A convention for mapping a code block to its solution file, e.g. an HTML comment above each block. |
