---
name: session-wrapup
description: Run at the end of a conversation to save project memory. Summarizes the session's work, updates the project tracker, and records any new lessons learned.
---

# Session Wrapup

The tracker and lessons learned files serve as the project's long-term memory. This workflow updates them so the next session can pick up right where this one left off.

## Steps

1. **Review Session Accomplishments:**
   Briefly reflect on what was built, fixed, analyzed, or discovered during the current conversation.

2. **Update `PROJECT_TRACKER.md`:**
   - **🟢 LIVE Sections:** Overwrite `§7 — Current Status`, `§8 — Open Questions & Blockers`, and `§9 — Next Actions` to reflect the reality at the end of this session.
   - **📜 APPEND-ONLY Sections:** 
     - If a major architectural or strategy decision was made, append it to `§10 — Decision Log` (Format: `D-NNN | Date | Decision | Rationale | Affects §`).
     - Append a new entry to `§11 — Session Changelog` summarizing the work (Format: `S-NNN | Date | Version | Notes`).

3. **Update `LESSONS_LEARNED.md`:**
   - If any new technical insights, gameplay strategies, tricky bugs, or mistakes were uncovered during the session, append them to the appropriate section in `LESSONS_LEARNED.md`. If no new distinct lessons were learned, skip this step.

4. **Report & Commit Message:**
   - Output a short, terse summary (in caveman style) to the user confirming the files have been updated and listing the key takeaways recorded for the next session.
   - Provide a suggested `git commit` message summarizing the work done in the session so the user can easily commit and push.
