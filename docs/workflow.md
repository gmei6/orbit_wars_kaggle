---
type: Playbook
title: Agent Operating Workflow
description: How an agent should plan, ground answers, build, and review in this repo.
tags: [agent, workflow, routing]
timestamp: 2026-06-16
---

# Grounding (before answering architecture or implementation questions)

1. Read [`/index.md`](/index.md), then open the relevant module doc under
   [`/architecture/`](/architecture/).
2. Ground the answer in that doc's `resource:` path. Open the code only to
   confirm a specific line — not to reconstruct the whole picture by grep.
3. If no module doc exists for the area, that is the bug. Write the doc first.

# Building

`ponytail` governs build decisions. Climb the ladder, stop at the first rung
that holds: does it need to exist (YAGNI) → stdlib → native feature →
installed dependency → one line → minimum code that works. Default level
`full`.

# Reviewing

Compose the review skills rather than free-forming:

- `ponytail-review` — flags over-engineering, dead abstractions, needless deps.
- `caveman-review` — one finding per line: `L<line>: <severity> <problem>. <fix>.`

This pair *is* the "terse math/code review" — no custom review prompt needed.

# Talking

`caveman` governs prose: terse, no filler, full technical accuracy. Default
level `lite` (professional, tight); bump to `full`/`ultra` for log-heavy work.
Code, commits, and security warnings are always written normally.

# Upgrade path

This map is hand-maintained. When the repo grows large enough that stale docs
start costing you, replace the manual map with auto-generated module docs +
structure maps with line-level evidence — see
`study8677/antigravity-workspace-template` (`ag-refresh` / `ag-ask`).
ponytail: hand map until staleness actually hurts, then automate.
