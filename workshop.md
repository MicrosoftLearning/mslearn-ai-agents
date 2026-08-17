---
title: Workshop agenda
permalink: workshop.html
---

{%- comment -%}
Workshop view. Every lab, task, timing and level on this page is read from the
frontmatter of the pages under /Instructions/Consolidated/, so it cannot drift
from the labs themselves. Nothing here is hard-coded.

Layout deliberately echoes a docs-style workshop site: a nav rail on the left
and the agenda on the right.
{%- endcomment -%}

{%- assign consolidated = site.pages | where_exp: "p", "p.url contains '/Instructions/Consolidated/'" -%}
{%- assign labs = consolidated | where_exp: "p", "p.lab.type == 'lab'" | sort: "lab.order" -%}
{%- assign all_tasks = consolidated | where_exp: "p", "p.lab.type == 'task'" -%}

<style>
.wk-wrap { display: grid; grid-template-columns: 15rem 1fr; gap: 2.5rem; align-items: start; }
@media (max-width: 900px) { .wk-wrap { grid-template-columns: 1fr; } }

.wk-nav { position: sticky; top: 1rem; font-size: .9em; border-right: 1px solid #e4e4e7; padding-right: 1rem; }
.wk-nav h4 { margin: 0 0 .5rem; font-size: .75em; letter-spacing: .08em; text-transform: uppercase; color: #6b7280; }
.wk-nav ol { list-style: none; margin: 0 0 1.25rem; padding: 0; }
.wk-nav li { margin: 0 0 .35rem; }
.wk-nav a { text-decoration: none; }
.wk-nav a:hover { text-decoration: underline; }
.wk-nav .wk-time { color: #6b7280; font-size: .85em; }

.wk-lab { border: 1px solid #e4e4e7; border-radius: 8px; padding: 1rem 1.25rem; margin: 0 0 1.25rem; }
.wk-lab h3 { margin-top: 0; }
.wk-meta { font-size: .85em; color: #6b7280; margin: -.4rem 0 .9rem; }
.wk-step { display: grid; grid-template-columns: 1fr auto auto; gap: .75rem;
           padding: .45rem 0; border-top: 1px solid #f1f1f3; align-items: baseline; }
.wk-step:first-of-type { border-top: none; }
.wk-badge { font-size: .72em; padding: .12em .5em; border-radius: 999px; white-space: nowrap; }
.wk-core { background: #e8f0fe; color: #1a45a5; }
.wk-setup { background: #f1f1f3; color: #52525b; }
.wk-elapsed { color: #6b7280; font-size: .85em; white-space: nowrap; }
.wk-locked { color: #92400e; background: #fef3c7; }
.wk-optional-list { font-size: .92em; color: #3f3f46; margin-top: .85rem; }
</style>

<div class="wk-wrap" markdown="0">
<nav class="wk-nav">
  <h4>Workshop</h4>
  <ol>
    <li><a href="#agenda">Agenda</a></li>
    <li><a href="#before-you-start">Before you start</a></li>
  </ol>
  <h4>Sessions</h4>
  <ol>
  {%- for lab in labs -%}
    {%- assign lab_id = lab.lab.id -%}
    {%- assign core = all_tasks | where_exp: "p", "p.lab.parent == lab_id" | where_exp: "p", "p.lab.section == 'core'" -%}
    {%- assign mins = 0 -%}
    {%- for t in core %}{% assign mins = mins | plus: t.lab.duration %}{% endfor -%}
    <li><a href="#lab-{{ lab_id | downcase }}">{{ lab.lab.title }}</a><br><span class="wk-time">{{ mins }} min core</span></li>
  {%- endfor -%}
  </ol>
  <h4>Other views</h4>
  <ol>
    <li><a href="{{ '/explore.html' | relative_url }}">Task explorer</a></li>
    <li><a href="{{ '/index.html' | relative_url }}">Full lab catalogue</a></li>
  </ol>
</nav>

<div class="wk-main" markdown="1">

# AI agents workshop

A guided, instructor-led path through the Tailwind Traders labs. Each session builds a
working agent, then hands off to the next.

This page is the **core path**: the shortest route through every lab that still ends with
something running. Optional tasks are listed under each session for anyone who finishes early
or wants to go further afterwards.

{%- assign total_core = 0 -%}
{%- assign total_all = 0 -%}
{%- for t in all_tasks -%}
  {%- if t.lab.duration -%}
    {%- assign total_all = total_all | plus: t.lab.duration -%}
    {%- if t.lab.section == 'core' %}{% assign total_core = total_core | plus: t.lab.duration %}{% endif -%}
  {%- endif -%}
{%- endfor -%}
{%- assign core_h = total_core | divided_by: 60 -%}
{%- assign core_m = total_core | modulo: 60 -%}
{%- assign all_h = total_all | divided_by: 60 -%}
{%- assign all_m = total_all | modulo: 60 -%}

**Core path:** {{ labs.size }} sessions, about **{% if core_h > 0 %}{{ core_h }}h {% endif %}{{ core_m }}m** of
hands-on time. **Everything**, including all optional tasks: about **{{ all_h }}h {% if all_m > 0 %}{{ all_m }}m{% endif %}**.

## Agenda
{: #agenda }

{% assign elapsed = 0 %}
{%- for lab in labs -%}
{%- assign lab_id = lab.lab.id -%}
{%- assign tasks = all_tasks | where_exp: "p", "p.lab.parent == lab_id" | sort: "lab.order" -%}
{%- assign core = tasks | where_exp: "p", "p.lab.section == 'core'" -%}
{%- assign optional = tasks | where_exp: "p", "p.lab.section == 'optional'" -%}
{%- assign setup = tasks | where_exp: "p", "p.lab.section == 'setup'" -%}
{%- assign lab_core = 0 -%}
{%- for t in core %}{% assign lab_core = lab_core | plus: t.lab.duration %}{% endfor -%}

<div class="wk-lab" markdown="0" id="lab-{{ lab_id | downcase }}">
  <h3><a href="{{ lab.url | relative_url }}">Session {{ lab.lab.order }} &mdash; {{ lab.lab.title }}</a></h3>
  <p class="wk-meta">{{ lab_core }} min core &middot; L{{ lab.lab.level }} &middot; {{ lab.lab.concepts }}</p>

  {%- for t in setup %}
  <div class="wk-step">
    <span><a href="{{ t.url | relative_url }}">{{ t.lab.title }}</a></span>
    <span class="wk-badge wk-setup">setup</span>
    <span class="wk-elapsed">before you start</span>
  </div>
  {%- endfor -%}

  {%- for t in core %}
  {%- assign elapsed = elapsed | plus: t.lab.duration -%}
  {%- assign e_h = elapsed | divided_by: 60 -%}
  {%- assign e_m = elapsed | modulo: 60 -%}
  <div class="wk-step">
    <span><a href="{{ t.url | relative_url }}">{{ t.lab.title }}</a></span>
    <span class="wk-badge wk-core">{{ t.lab.duration }} min</span>
    <span class="wk-elapsed">{% if e_h > 0 %}{{ e_h }}h {% endif %}{{ e_m }}m elapsed</span>
  </div>
  {%- endfor -%}

  {%- if optional.size > 0 %}
  <div class="wk-optional-list" markdown="0">
    <strong>Optional, if there's time:</strong>
    <ul>
    {%- for t in optional %}
      <li><a href="{{ t.url | relative_url }}">{{ t.lab.title }}</a> &middot; {{ t.lab.duration }} min &middot; L{{ t.lab.level }}
      {%- if t.lab.access == 'gated' %} <span class="wk-badge wk-locked">demo only &mdash; {{ t.lab.requires }}</span>{% endif -%}
      </li>
    {%- endfor %}
    </ul>
  </div>
  {%- endif %}
</div>
{%- endfor %}

## Before you start
{: #before-you-start }

Each session has its own **Getting started** page covering the Microsoft Foundry project,
starter code and environment for that lab. Attendees should complete the one for session 1
before the workshop begins:

{% for lab in labs -%}
{%- assign lab_id = lab.lab.id -%}
{%- assign setup = all_tasks | where_exp: "p", "p.lab.parent == lab_id" | where_exp: "p", "p.lab.section == 'setup'" -%}
{%- for s in setup %}
- **{{ lab.lab.title }}** &mdash; [{{ s.lab.title }}]({{ s.url | relative_url }})
{%- endfor -%}
{%- endfor %}

{% assign gated = all_tasks | where_exp: "p", "p.lab.access == 'gated'" | sort: "lab.parent" %}
{%- if gated.size > 0 %}
### Tasks that need extra access

{{ gated.size }} optional tasks need permissions or licensing many attendees won't have, so
they're **demo only** in a workshop setting. Nothing else depends on them.

| Task | Needs |
| --- | --- |
{% for t in gated -%}
| [{{ t.lab.title }}]({{ t.url | relative_url }}) | {{ t.lab.requires }} |
{% endfor %}
{%- endif %}

</div>
</div>
