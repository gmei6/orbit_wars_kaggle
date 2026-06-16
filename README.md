# Reusable Coding / Math Workspace Template

A general-purpose starting point for coding and quantitative work, built from
three real pieces:

- **[ponytail](https://github.com/DietrichGebert/ponytail)** — the "laziest
  senior dev" skill; governs *what you build* (minimal, stdlib-first, YAGNI).
- **[caveman](https://github.com/JuliusBrussee/caveman)** — token-compression
  skill; governs *how you talk* (terse, full accuracy).
- **[OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)**
  — Google Cloud's Open Knowledge Format; the `docs/` folder is an OKF bundle
  (Markdown + YAML frontmatter) the agent reads before touching code.

## Layout

```
AGENTS.md / CLAUDE.md / GEMINI.md   # agent entry points (import the skills)
docs/                               # OKF v0.1 knowledge bundle
  index.md                          # bundle root (only place okf_version lives)
  workflow.md  conventions.md       # operating loop + hard constraints
  architecture/                     # one doc per module, bound to a code path
github-steals/                      # the real ponytail + caveman skills (vendored)
addons/quant/                       # OPTIONAL numeric add-on (seeding + oracle)
scripts/check_okf.py                # OKF conformance checker
```

## How each tool loads it

- **Claude Code / Cowork** reads `CLAUDE.md`, which `@`-imports ponytail and
  caveman so they're active every response.
- **Google Antigravity / Gemini CLI** reads `GEMINI.md`, same imports.
- **Other agents**: `npx skills add JuliusBrussee/caveman` /
  `npx skills add DietrichGebert/ponytail`.

The skills are *referenced*, not duplicated — you get upstream updates and the
tuned intensity levels (`/ponytail lite|full|ultra`, `/caveman …`) for free.

## Reusing the template

1. Copy this folder per project.
2. Add a module doc under `docs/architecture/` (copy `_module-template.md`) for
   each real module; set its `resource:` to the code path.
3. Keep code general. The `addons/quant/` folder (deterministic seeding, oracle
   baselines) is opt-in — delete it for non-numeric projects.
4. Run `python scripts/check_okf.py docs` before committing knowledge changes.

## What changed from the first draft

- `project.yaml` deprecated (it's not part of OKF) — left as a tombstone you
  can delete. Version now lives only in `docs/index.md` frontmatter (spec §11),
  and every concept doc carries the required `type` field (spec §9).
- Folder fixed to `.agents/` (plural) for Antigravity; the singular `.agent/`
  is not discovered.
- ponytail/caveman are imported from `github-steals/`, not paraphrased into
  hand-written files.
- The C++/JAX/GARCH specifics were moved out of the base into the optional
  `addons/quant/` so the template stays reusable for general coding and math.
