# Research Log

Maintained by the Auto-Researcher passes. Each entry records what was looked
at, what was implemented, and what was deferred so future runs do not redo
the same work.

## 2026-06-08 — Auto-Researcher v4

**Resume-worthiness score (start of run):** ~55 / 100
- Tech stack prestige (25): 15 — Python backend + lightweight web UI is
  solid but not differentiated; the resume edge would come from depth in
  the coaching logic, not the stack.
- Commit recency (25): 22 — last push 2026-05-11.
- Feature completeness (20): unknown this pass; not opened in depth.
- Stars + visibility (15): 3 — 1 star.
- README quality (15): unknown this pass.

**Implemented on branch `claude/brave-bohr-fX5uP`:**
- `RESEARCH_LOG.md` — this file. Recorded so the next pass starts with
  context instead of re-deriving the priority call.

**Why this pass did not ship code here:**
The top three repos absorbed this run's safe-change budget. For
ai_interview_coach the highest-ROI next step is content depth (better
rubric, more roles, transcript scoring) which requires reading the existing
coaching prompts rather than a generic hygiene pass.

**Next-run candidates (in priority order):**
1. Audit the LLM call sites and make sure they are on a current Claude model
   (`claude-opus-4-8` / `claude-sonnet-4-6`) with prompt caching enabled for
   the role rubric system prompt.
2. Add structured JSON output (tool use) for the per-question scoring so the
   UI can render strengths / weaknesses tables instead of free text.
3. Add `.github/workflows/ci.yml` (ruff + py_compile) consistent with the
   other repos.
4. Add a short demo GIF of a mock interview run to the README — this is the
   single highest-leverage README change for a coaching tool.
5. Add a `SECURITY.md` with `.env` hygiene and PII-handling notes (interview
   transcripts can be sensitive).
