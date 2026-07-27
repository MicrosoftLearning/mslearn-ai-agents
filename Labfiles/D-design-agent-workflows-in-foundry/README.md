# Lab D — Design agent workflows in Microsoft Foundry (files)

Starter assets for the **Design agent workflows in Microsoft Foundry** lab, reskinned to
the **Tailwind Traders** scenario (an outdoor-gear retailer that also runs guided trips).
You design a customer-support **ticket classification and routing workflow** in the
Foundry visual workflow designer, then optionally drive it from a client app.

Most of this lab is built **in the Foundry portal** — there's very little code. The files
here are the copy/paste assets for the portal steps, plus an optional client app.

```
D-design-agent-workflows-in-foundry/
├─ assets/
│  ├─ sample_tickets.json   # the ticket array for the Set variable node
│  └─ agent-prompts.md      # triage + resolution prompts, JSON schema, node messages
├─ Python/                  # starter for the optional client-app task (D4)
│  ├─ workflow.py           #   fill-in-the-blanks workflow invoker (console)
│  ├─ tailwind_ui.py        #   shared Gradio chat shell (provided; not edited)
│  ├─ requirements.txt
│  └─ .env.example
└─ Solution/
   ├─ Python/               # finished client-app code
   │  ├─ workflow.py        #   console version (complete)
   │  ├─ workflow_ui.py     #   optional web-chat version (Gradio shell)
   │  ├─ tailwind_ui.py
   │  ├─ requirements.txt
   │  └─ .env.example
   └─ README.md             # how to run the solution + no-Azure sanity checks
```

## Instruction pages

Start with the landing page and getting-started, then do the core task and any optional tasks:

| Page | What it covers |
| --- | --- |
| `Instructions/Exercises/D-design-agent-workflows-in-foundry.md` | Lab overview |
| `Instructions/Exercises/D0-getting-started.md` | One-time setup / prerequisites |
| `Instructions/Exercises/D1-classify-and-route-a-ticket.md` | **Core** — classify + route a ticket |
| `Instructions/Exercises/D2-handle-low-confidence-tickets.md` | *Optional* — low-confidence handling |
| `Instructions/Exercises/D3-generate-recommended-responses.md` | *Optional* — recommended responses |
| `Instructions/Exercises/D4-call-your-workflow-from-a-client-app.md` | *Optional* — client app |

## The Tailwind Traders scenario

Support tickets are classified into one of three categories:

- **Billing** — a customer was charged, refunded, or paid incorrectly. Routed to the human orders team.
- **Gear** — faulty equipment or product setup/usage problems. Handled automatically.
- **General** — how-to questions, availability, order history, returns. Handled automatically.
