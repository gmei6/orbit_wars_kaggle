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

Defaults: ponytail **full**, caveman **lite**. Follow `docs/workflow.md`; honor
`docs/conventions.md`.

For slash-command skills inside Antigravity, place skill files under
`.agents/skills/` (see `.agents/skills/README.md`) or run
`npx skills add JuliusBrussee/caveman -a antigravity`.
