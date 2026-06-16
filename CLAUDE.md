# CLAUDE.md

Project memory for Claude Code / Cowork. The contract lives in AGENTS.md; the
two behavior skills are imported below so they are active every response.

@./AGENTS.md

# Active skills

@./github-steals/ponytail-skills/skills/ponytail/SKILL.md
@./github-steals/caveman/skills/caveman/SKILL.md

# Defaults

Operate ponytail **full**, caveman **lite** unless I say otherwise
(`/ponytail …`, `/caveman …`, or `normal mode`).

# Reviewing

For code or math review, load the review skills on demand — do not free-form:

- `github-steals/ponytail-skills/skills/ponytail-review/SKILL.md`
- `github-steals/caveman/skills/caveman-review/SKILL.md`

To make them auto-invoke, copy those two SKILL dirs into `.claude/skills/`, or
run `npx skills add DietrichGebert/ponytail` and
`npx skills add JuliusBrussee/caveman`.

# Knowledge

Follow `docs/workflow.md`. Honor `docs/conventions.md` (deterministic seeding,
oracle protection). Knowledge before code: ground answers in the module docs.
