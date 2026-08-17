---
title: Task explorer
permalink: explore.html
layout: workshop
sitemap: false
---

{%- comment -%}
Task explorer. Lists every consolidated task and filters client-side using the
data- attributes on each card.
{%- endcomment -%}

{%- assign consolidated = site.pages | where_exp: "p", "p.url contains '/Instructions/Consolidated/'" -%}
{%- assign labs = consolidated | where_exp: "p", "p.lab.type == 'lab'" | sort: "lab.order" -%}
{%- assign tasks = consolidated | where_exp: "p", "p.lab.type == 'task'" | sort: "lab.order" -%}

# Task explorer

Every task across the consolidated labs. Filter by lab, section, level, time or access to
find the ones that fit.

<div class="ex-filters" markdown="0">
  <div>
    <label for="f-lab">Lab</label>
    <select id="f-lab">
      <option value="">All labs</option>
      {%- for lab in labs %}
      <option value="{{ lab.lab.id }}">{{ lab.lab.title }}</option>
      {%- endfor %}
    </select>
  </div>
  <div>
    <label for="f-section">Section</label>
    <select id="f-section">
      <option value="">Core and optional</option>
      <option value="core">Core only</option>
      <option value="optional">Optional only</option>
      <option value="setup">Setup</option>
    </select>
  </div>
  <div>
    <label for="f-level">Level</label>
    <select id="f-level">
      <option value="">Any level</option>
      <option value="200">L200</option>
      <option value="300">L300</option>
      <option value="400">L400</option>
    </select>
  </div>
  <div>
    <label for="f-time">Time</label>
    <select id="f-time">
      <option value="">Any length</option>
      <option value="20">20 min or less</option>
      <option value="30">30 min or less</option>
    </select>
  </div>
  <div>
    <label for="f-access">Access</label>
    <select id="f-access">
      <option value="">All tasks</option>
      <option value="open">No extra access needed</option>
      <option value="gated">Needs extra access</option>
    </select>
  </div>
</div>

<p class="ex-count" id="ex-count"></p>

<div class="ex-grid" id="ex-grid" markdown="0">
{%- for t in tasks -%}
{%- assign parent = labs | where_exp: "l", "l.lab.id == t.lab.parent" | first -%}
  <article class="ex-card"
           data-lab="{{ t.lab.parent }}"
           data-section="{{ t.lab.section }}"
           data-level="{{ t.lab.level }}"
           data-duration="{{ t.lab.duration | default: 0 }}"
           data-access="{{ t.lab.access }}">
    <h4><a href="{{ t.url | relative_url }}">{{ t.lab.title }}</a></h4>
    <p>{{ t.lab.description }}</p>
    <div class="ex-tags">
      <span class="ex-tag">{{ parent.lab.title }}</span>
      <span class="ex-tag {% if t.lab.section == 'core' %}core{% endif %}">{{ t.lab.section }}</span>
      {%- if t.lab.difficulty %}
      <span class="ex-tag ex-bars">{% for i in (1..5) %}{% if i <= t.lab.difficulty %}&#9648;{% else %}&#9649;{% endif %}{% endfor %} L{{ t.lab.level }}</span>
      {%- endif %}
      {%- if t.lab.duration %}<span class="ex-tag">{{ t.lab.duration }} min</span>{% endif %}
      {%- if t.lab.access == 'gated' %}<span class="ex-tag gated">needs access</span>{% endif %}
    </div>
  </article>
{%- endfor %}
</div>

<p class="ex-empty" id="ex-empty" style="display:none">No tasks match those filters.</p>

<script>
(function () {
  var grid = document.getElementById('ex-grid');
  var cards = Array.prototype.slice.call(grid.querySelectorAll('.ex-card'));
  var count = document.getElementById('ex-count');
  var empty = document.getElementById('ex-empty');
  var filters = ['lab', 'section', 'level', 'time', 'access'].map(function (id) {
    return document.getElementById('f-' + id);
  });

  function apply() {
    var lab = filters[0].value, section = filters[1].value, level = filters[2].value;
    var time = filters[3].value, access = filters[4].value;
    var shown = 0;

    cards.forEach(function (card) {
      var d = card.dataset;
      var ok = (!lab || d.lab === lab)
        && (!section || d.section === section)
        && (!level || d.level === level)
        && (!time || (parseInt(d.duration, 10) > 0 && parseInt(d.duration, 10) <= parseInt(time, 10)))
        && (!access || d.access === access);
      card.style.display = ok ? '' : 'none';
      if (ok) { shown++; }
    });

    count.textContent = shown + ' of ' + cards.length + ' tasks';
    empty.style.display = shown === 0 ? '' : 'none';
  }

  filters.forEach(function (f) { f.addEventListener('change', apply); });
  apply();
})();
</script>
