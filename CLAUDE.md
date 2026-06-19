---
type: Configuration
---

# CLAUDE.md

Project memory for Claude Code / Cowork. The contract lives in AGENTS.md; the
two behavior skills are imported below so they are active every response.

@./PROJECT_TRACKER.md
@./AGENTS.md

# Active skills

@./github-steals/ponytail-skills/skills/ponytail/SKILL.md
@./github-steals/caveman/skills/caveman/SKILL.md

# Defaults

Operate ponytail **full**, caveman **lite** unless I say otherwise
(`/ponytail …`, `/caveman …`, or `normal mode`).

# Code layout

- `v1/` — **frozen baseline**. Don't edit it to chase new behavior; it's the
  reference opponent the arena measures against (`targeting.py` is the brain,
  `strategy.py` a pass-through).
- `v2_1/` — **active development**. Make changes here (`strategy.py` is the
  brain, `targeting.py` is the pure-math oracle). Lineage: `v1_1` → `v2_macro`
  → `v2_1`; the old `v1_1/` dir no longer exists.
- `v2_macro/` — **frozen prior baseline**. The v2 arena yardstick; don't edit.
- `v(teamwork-preview)/` — experimental variant, off the main line.
- `scripts/` — `arena.py` (self-play eval), `sim.py` (local engine),
  `check_okf.py` (docs conformance). `vendor/` holds the Kaggle env.

# Reviewing

For code or math review, load the review skills on demand — do not free-form:

- `github-steals/ponytail-skills/skills/ponytail-review/SKILL.md`
- `github-steals/caveman/skills/caveman-review/SKILL.md`

To make them auto-invoke, copy those two SKILL dirs into `.claude/skills/`, or
run `npx skills add DietrichGebert/ponytail` and
`npx skills add JuliusBrussee/caveman`.

# Knowledge

Follow `docs/workflow.md`. Honor `docs/conventions.md` (deterministic seeding,
oracle protection). Knowledge before code: ground answers in the module docs
under `docs/architecture/` before grepping.
