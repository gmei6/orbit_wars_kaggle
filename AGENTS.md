# Agent Operating Contract

This workspace pairs two behavior skills with an OKF knowledge layer. The
skills are the real upstream skills, vendored in [`github-steals/`](github-steals/)
— referenced, not re-copied, so there is nothing to keep in sync.

## Skills

- **ponytail** — governs *what you build*: laziest solution that works, stdlib
  before dependencies, YAGNI. Default level: `full`.
- **caveman** — governs *how you talk*: terse prose, no filler, full technical
  accuracy. Default level: `lite`. Code, commits, and security warnings stay
  normal.

They compose cleanly: ponytail for decisions and code, caveman for the prose
around it. Switch with `/ponytail lite|full|ultra` and
`/caveman lite|full|ultra`; `normal mode` turns a skill off.

For review, compose `ponytail-review` + `caveman-review` instead of writing a
custom review prompt.

## Knowledge layer (OKF v0.1)

Read [`PROJECT_TRACKER.md`](PROJECT_TRACKER.md) first to align with current session goals. Then read [`docs/index.md`](docs/index.md). Before answering architecture or
implementation questions, open the relevant module doc under
[`docs/architecture/`](docs/architecture/) and ground claims in its `resource:`
path before grepping code. Hard constraints live in
[`docs/conventions.md`](docs/conventions.md); the operating loop is in
[`docs/workflow.md`](docs/workflow.md).

## Loading the skills

- **Claude Code / Cowork** → [`CLAUDE.md`](CLAUDE.md) imports them.
- **Antigravity / Gemini CLI** → [`GEMINI.md`](GEMINI.md) imports them.
- **Any other agent** → `npx skills add JuliusBrussee/caveman` and
  `npx skills add DietrichGebert/ponytail`, or copy the SKILL.md dirs into that
  agent's skills folder.
