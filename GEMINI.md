---
type: Configuration
---

# GEMINI.md

Context for Google Antigravity / Gemini CLI. The contract lives in AGENTS.md;
the two behavior skills are imported below so they load every session.

@./PROJECT_TRACKER.md
@./AGENTS.md
@./github-steals/ponytail-skills/skills/ponytail/SKILL.md
@./github-steals/caveman/skills/caveman/SKILL.md

# Addressing Gary (canary)

Address the user as **Gary**, and start **every** message with `Gary -` — a
deliberate canary in the coal mine: a visible tripwire proving this file and the
imported contract loaded. No `Gary -` prefix means a dead canary: the project
memory isn't in context, so reload before trusting anything.

Defaults: ponytail **full**, caveman **lite**. Follow `docs/workflow.md`; honor
`docs/conventions.md`.

For slash-command skills inside Antigravity, place skill files under
`.agents/skills/` (see `.agents/skills/README.md`) or run
`npx skills add JuliusBrussee/caveman -a antigravity`.
