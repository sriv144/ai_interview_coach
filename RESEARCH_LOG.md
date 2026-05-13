# Research Log

This log tracks automated research and improvement runs by the
auto-researcher agent.

---

## 2026-05-13 — Auto-Researcher v4

**Resume score at start of run:** 55 / 100
- Tech stack prestige: 12/25 (Python web UI + LLM career tool)
- Commit recency: 25/25 (active within the last 48 hours)
- Feature completeness: 10/20
- Stars + visibility: 4/15
- README quality: 4/15

**Implemented (branch: `claude/brave-bohr-HHSYf`):**
- `RESEARCH_LOG.md` (this file) so future runs can avoid duplicate work.

**Why no code changes this run:**
- This repo has the lowest resume score of the six targets and the
  remaining token budget was better spent on the higher-leverage repos.
- The README and feature surface are thin enough that a meaningful
  improvement would be a feature pass (e.g. role-specific question
  bank + Claude scoring), which is not a one-commit job.

**Next-run candidates (ranked):**
1. README overhaul: hero image, runnable quick-start, screenshot of
   the UI, sample interview transcript.
2. Add `.github/workflows/ci.yml` + a minimal pytest scaffold.
3. Replace any OpenAI-only path with an Anthropic Claude option using
   `claude-sonnet-4-6` for question generation and feedback scoring.
4. Add a role-specific question bank (`SWE`, `data-eng`, `pm`, `mle`)
   and a Claude-scored rubric per role.
5. Persist sessions with SQLite + a streak/history view.
