---
okf_version: "0.1"
---

# Project Knowledge

OKF v0.1 knowledge bundle for this workspace: plain Markdown + YAML
frontmatter, readable by humans and agents, diffable in git. This file is the
entry point — open it before grepping code.

This is the only file in the bundle that carries an `okf_version` (per spec
§11). Every other concept document declares a `type`.

# Operating Knowledge

* [Workflow](/workflow.md) - how an agent should plan, ground answers, build, and review here
* [Conventions](/conventions.md) - non-negotiable constraints: reproducibility, oracle protection

# Architecture

* [Modules](/architecture/) - one knowledge doc per module, each bound to a code path

# Design

* [v2 Information Model & Strategy](/design/v2-information-model.md) - how state is stored (forecastable baseline, event timeline) plus the v2 doctrine and staged build plan

# Add-ons

* [Quant / numeric add-on](/../addons/quant/index.md) - optional; keep out of general projects
