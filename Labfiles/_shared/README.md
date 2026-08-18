# Shared lab infrastructure

Every consolidated lab ships the same optional `azd` template: the same Bicep,
the same post-provision scripts, the same `azure.yaml`. Those files live here
once, and `sync.py` copies them into each lab.

## Why copies rather than a shared path

Each lab folder has to be self-contained. A learner downloads or opens one lab
and everything it needs is inside it — no path traversal, no shared folder they
didn't know to fetch. Pointing `azure.yaml` at `../_shared/infra` would work for
`azd` but break that, and adds a concept to explain in the instructions.

So the duplication is deliberate. What isn't acceptable is *silent* duplication:
before this, `main.bicep` and `resources.bicep` were byte-identical across three
labs with nothing to tell you when one was updated and the others weren't.

## Making a change

1. Edit the canonical file here, under `Labfiles/_shared/`.
2. Run the sync:

   ```
   python Labfiles/_shared/sync.py
   ```

3. Commit both the canonical file and the regenerated copies.

CI runs `sync.py --check` on every pull request, so a copy that drifts — or a
canonical file changed without syncing — fails the build with a diff.

The generated copies carry a header saying they're generated. `main.parameters.json`
doesn't, because JSON has no comment syntax; it's still checked.

## Adding a lab

Add an entry to `manifest.yml` and run the sync:

```yaml
labs:
  D-observe-evaluate-and-secure-agents:
    azd_name: caldova-observability-lab
    description: the Caldova observability lab
    hint: >-
      Task 2 needs a grounded agent to evaluate: from the Python folder, run
      'python ../setup/bootstrap_agent.py' to create one.
```

The lab folder must already exist. Nothing else is required — the Bicep,
`azure.yaml` and both `write_env` scripts are generated for it.

## What is and isn't managed here

| Managed | Not managed |
| --- | --- |
| `infra/main.bicep` | `setup/check_env.py` |
| `infra/resources.bicep` | `setup/bootstrap_agent.py` |
| `infra/main.parameters.json` | `Python/requirements.txt` |
| `setup/write_env.ps1` | `Python/**` and `Solution/**` |
| `setup/write_env.sh` | |
| `azure.yaml` | |

The right-hand column is genuinely lab-specific: `check_env.py` validates that
lab's tasks, `bootstrap_agent.py` creates that lab's agent, and requirements
differ per lab. Those are left alone on purpose.

## Tokens

Three files vary slightly between labs, so they're templated. Values come from
`manifest.yml`:

| Token | Used in | Example |
| --- | --- | --- |
| `{{LAB_FOLDER}}` | `azure.yaml` | `A-build-and-extend-ai-agents` |
| `{{AZD_NAME}}` | `azure.yaml` | `caldova-lab` |
| `{{LAB_DESCRIPTION}}` | `azure.yaml` | `the Caldova lab` |
| `{{LAB_HINT}}` | `write_env.ps1`, `write_env.sh` | the closing line telling the learner what else that lab needs |

An unresolved token is an error, so a lab added to `manifest.yml` without all of
its values fails loudly rather than shipping `{{AZD_NAME}}` to a learner.
