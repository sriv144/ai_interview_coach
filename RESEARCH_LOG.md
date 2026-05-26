# Research Log

This log tracks autonomous-agent improvements (auto-researcher runs).
Each entry records what was implemented, why, what was skipped, and
candidates for future runs.

## 2026-05-26 — Auto-Researcher v4

**Resume score at run start:** 50/100
(AI interview prep tool, Python backend + lightweight web UI,
1 star, last commit 2026-05-11)

### Implemented (branch: `claude/brave-bohr-DU4LA`)
- Bootstrap log entry only. No source changes shipped this run.

### Why deferred
- Token budget this run targeted the top 3 repos by resume score.
- The interesting question for this repo is whether the underlying
  feedback loop (audio → transcript → rubric scoring) is compelling.
  Adding scaffolding before validating that flow would be premature.

### Next-run candidates
- Read backend + UI, document the feedback rubric and which model
  performs the scoring.
- If using a non-Anthropic model, migrate scoring to Claude and
  showcase reasoning quality.
- Add CI workflow (lint + unit tests).
- README upgrade: screenshots / demo GIF of the interview practice
  flow; a fresh-clone time-to-first-feedback target of <5 min.
