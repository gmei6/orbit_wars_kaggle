# .agents/skills/

Google Antigravity discovers project skills here (note the **plural** —
`.agents/`, not `.agent/`). A Markdown file at `.agents/skills/lint.md` becomes
the `/lint` command in the Antigravity TUI.

This template wires ponytail and caveman through `@`-imports in `GEMINI.md`
instead, because both are *always-on* behavior modes ("active every response"),
which suits an imported context file better than an on-demand slash command.

If you do want them as slash commands here, either:

- copy the SKILL.md files from `../../github-steals/` into this folder, or
- run `npx skills add JuliusBrussee/caveman -a antigravity` and
  `npx skills add DietrichGebert/ponytail -a antigravity`.

Project-level alternative location Antigravity also reads: `.antigravity/skills/`.
Global skills live at `~/.gemini/antigravity-cli/skills/`.
