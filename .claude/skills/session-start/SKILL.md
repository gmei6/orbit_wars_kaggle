---
name: session-start
description: Run at the start of every new conversation to load project memory. Reads the tracker and docs, restates the Goal, and surfaces current status, open questions, and next actions before any work begins.
---

# Session Start

The tracker is the project's memory across conversations. Load it before doing anything.

## Steps
1. Read `PROJECT_TRACKER.md` in this order: Goal → Current State → Active Session → Rules of Engagement.
2. Read `docs/workflow.md` and `docs/conventions.md` to ground the rules of engagement and development loop.
3. Report a short orientation:
   - The Goal in one sentence (confirm it is intact).
   - Current phase and the latest validated result from the Tracker.
   - Open questions / blockers.
   - The next 1–3 concrete actions.
4. Ask what the user wants to tackle, and flag immediately if their intent conflicts with the Goal or a prior decision — surface the tension before proceeding.

Read-and-orient only. This workflow edits nothing.
