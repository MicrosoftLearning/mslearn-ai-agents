---
title: 'Observe, evaluate, and secure your agents'
lab:
    title: 'Observe, evaluate, and secure your agents'
    description: 'Find out what your Caldova agent is actually doing: trace it with OpenTelemetry, score its answers against ground truth with built-in evaluators, and attack it with the AI Red Teaming Agent. A modular lab you can complete end to end or one task at a time.'
    type: 'lab'
    id: 'D'
    order: 4
    difficulty: 3
    duration: 60
    access: 'open'
    level: 300
    concepts: 'tracing, OpenTelemetry, evaluation, groundedness, AI red teaming'
    islab: true
    status: 'draft'
---

<!--
PILOT NOTE (remove before publishing):
"Lab D" is new content: there was no observability, evaluation or safety-testing
material anywhere in this repo. It follows the same template as Labs A-C.
Starter code lives in a single folder — Labfiles/D-observe-evaluate-and-secure-agents/Python/ —
shared by every task (one virtual environment, one .env). The completed reference code is
in Labfiles/D-observe-evaluate-and-secure-agents/Solution/Python/.

This landing page is the lab overview. Setup lives in D0-getting-started.md and each task is
its own page (D1-D3) so it can be completed on its own. The azd template and Bicep are
generated from Labfiles/_shared/ — edit them there, not in the lab folder.
-->

# Observe, evaluate, and secure your agents

**Level** ▰▰▰▱▱ **L300**  (**L100** beginner → **L500** expert)

You can build an agent in an afternoon. Knowing whether it's any good — and whether it
behaves when someone tries to make it misbehave — is a different job. This lab is about
that job: seeing inside a running agent, measuring the quality of its answers, and
attacking it before someone else does.

![Anton](../Media/anton-avatar.png)<br /><strong>Meet Anton, your AI guide.</strong><br />You'll spot **Ask Anton** tips throughout this lab. Want more interactive, hands-on help? Chat with Anton in the *[Ask Anton](https://aka.ms/choose-anton)* app.

<details>
<summary><strong><i>About the Ask Anton app</i></strong></summary>

<strong><i><a href="https://aka.ms/choose-anton" target="_blank">Ask Anton</a></i></strong> is a generative AI agent that can answer questions about AI concepts and Microsoft Foundry technologies. It's available in two versions at <code>https://aka.ms/choose-anton</code>:
<ul>
<li><strong>Azure-based</strong>: Best experience <i>(requires an Azure subscription and deployment of a model in a Foundry project)</i>.</li>
<li><strong>Browser-based</strong>: Use a small language model in your browser <i>(reduced functionality - may be slow or work only in "basic" mode in older/lower-spec devices)</i>.</li>
</ul>
<blockquote><i>Ask Anton is <u>not</u> a supported Microsoft product or a component of Microsoft Learn or AI Skills Navigator.</i></blockquote>
</details>

<style>
/* "Ask Anton" just-in-time concept blocks */
details.concept { margin:.6rem 0 1rem; }
details.concept > summary { display:inline-block; cursor:pointer; list-style:none;
  font-size:.85em; font-weight:600; color:#6b4ba1; background:#6b4ba112;
  border:1px solid #6b4ba133; border-radius:999px; padding:.2em .7em; }
details.concept > summary::-webkit-details-marker { display:none; }
details.concept > summary::before { content:"Ask Anton: "; font-weight:700;
  padding-left:1.5em;
  background:url("../Media/anton-avatar.png") left center / 1.25em 1.25em no-repeat; }
details.concept > summary:hover { background:#6b4ba1; color:#fff; border-color:#6b4ba1; }
details.concept[open] > summary { border-bottom-left-radius:0; border-bottom-right-radius:0; }
details.concept .concept-body { border:1px solid #6b4ba133; border-top:none;
  border-radius:0 8px 8px 8px; padding:.6rem .9rem; background:#6b4ba108; font-size:.95em; }
</style>

<details markdown="1" class="concept">
<summary>Why can't I just read the output?</summary>
<div class="concept-body" markdown="1">

Because the output is the one part of an agent that looks fine when everything else isn't.
An answer can be fluent and confidently wrong, or correct but produced by three retries and
a tool call that timed out. **Tracing** shows you what happened on the way to the answer.
**Evaluation** scores the answer against something you already know to be true.
**Red teaming** tells you what the agent does when the question is hostile.

</div>
</details>

**Your scenario:** you work at **Caldova**, a pharmaceutical manufacturer preparing an
accelerated product launch. The supply chain assistant you built in earlier labs is now
answering real questions from planning teams — and the IT compliance lead is asking harder
questions about it. *Why was that answer slow? Is it making things up about the capacity
policy? What happens if someone tries to talk it into something it shouldn't say?* In this
lab you answer all three with evidence rather than opinion.

You'll start with the **Core** tasks, which get you from "it runs" to "I can prove how well
it runs". The **Optional** task then goes after safety.

> **Note**: Some of the technologies used in this exercise are in preview or in active
> development. You may experience some unexpected behavior, warnings, or errors.

## What you'll learn

By completing the **Core** tasks of this exercise, you'll be able to:

- **Trace an agent** with OpenTelemetry, export the traces to Azure Monitor, and read them
  in the Foundry portal — including custom spans you add around your own code.
- **Evaluate answer quality** against ground truth using built-in evaluators
  (groundedness, relevance, similarity) and a JSONL dataset.

The **Optional** task lets you additionally:

- **Red team your agent** with the AI Red Teaming Agent: run adversarial attack strategies
  and your own seed prompts against a deployed agent, and read the attack success rate.

## How this lab is organized

This lab is **modular**. Each task is written to be completed **on its own, starting fresh** —
so you can pick a single task and do just that one. Every task also shares one starter folder,
one virtual environment, and one `.env`, so if you'd rather work straight through, you can.

1. **Start with [Getting started](D0-getting-started.md)** — create your Microsoft Foundry
   project, connect Application Insights, get the starter code, and set up your `.env`. Every
   task begins from here; if you're doing the whole lab in one sitting, you only need to do
   this once.
2. **Do any task.** Each task lists the setup it needs so you can start it independently. If
   you're moving straight from the previous task, a short *"Continuing from a previous task?"*
   note at the top lets you skip the repeated setup and keep going.

## Lab at a glance

Complete the **Core** tasks first — they end with an agent you can see
inside and a scorecard for its answers. Then add the **Optional** task if you want to test
how it stands up to attack.

<!-- BEGIN GENERATED: task-table - do not edit by hand; run: python tools/generate_lab_blocks.py -->
| Section | Task | Level | Time |
| --- | --- | --- | --- |
| **Core** | [Task 1 – Trace your agent](D1-trace-your-agent.md) | ▰▰▰▱▱ L300 | ~25 min |
| **Core** | [Task 2 – Evaluate answer quality](D2-evaluate-answer-quality.md) | ▰▰▰▱▱ L300 | ~35 min |
| *Optional* | [Task 3 – Red team your agent](D3-red-team-your-agent.md) | ▰▰▰▰▱ L400 | ~35 min |

**Core tasks:** about **60 minutes**. **Full lab**, including every optional task: about **1 hour 35 minutes**.
<!-- END GENERATED: task-table -->

**Choosing your path** — pick the tasks that fit the time you have:

- **Core only (~1h):** do Tasks 1–2.
- **Everything (~1h 35m):** add **Task 3**, the red team scan.

> **One agent, three questions**: Task 1 traces an agent you create in code. Tasks 2 and 3
> both point at the **grounded knowledge agent** from
> [Lab B](B-integrate-agents-with-enterprise-knowledge-and-m365.md). If you haven't done Lab B,
> one command creates an equivalent agent so this lab stands alone — see
> [Getting started](D0-getting-started.md).

## Measure, don't guess

The three techniques in this lab answer different questions, and it's worth being clear about
which is which:

- **Tracing** answers *"what happened?"* It's a record of one run: which spans took how long,
  which tools were called, what the model was sent. Use it when something is slow or broke.
- **Evaluation** answers *"how good is it, on average?"* It's a score over a dataset, so it's
  the only one of the three that tells you whether a change made things better or worse.
- **Red teaming** answers *"what can I make it do?"* It's an adversarial probe, and a clean
  result is a floor, not a guarantee.

None of them replaces the others, and all three are cheap compared to finding out in
production.

## Summary

Across this lab you:

- **Instrumented an agent** with OpenTelemetry, exported traces to Application Insights, and
  read them — including your own custom spans — in the Foundry portal.
- **Evaluated a grounded agent** against a ground-truth dataset with built-in groundedness,
  relevance and similarity evaluators, and got a score you can compare across changes.
- (Optionally) **Red teamed the agent** with adversarial attack strategies and your own seed
  prompts, and read the resulting attack success rate.

Together these turn "the demo worked" into evidence you can show someone.

## Clean up

If you're finished, delete the resources you created to avoid unnecessary Azure costs.

1. In the [Azure portal](https://portal.azure.com), navigate to the resource group that contains your Foundry resource.
1. On the toolbar, select **Delete resource group**, enter the resource group name, and confirm.

> The code you run in Task 1 deletes the agent version it creates. The agent Tasks 2 and 3
> measure is removed when you delete the resource group. If you provisioned with `azd`, run
> `azd down` instead — but note that Application Insights, if you created it from the Foundry
> portal, is a separate resource and is deleted with the resource group rather than by `azd`.
