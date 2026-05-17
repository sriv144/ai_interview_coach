# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-05-17 — Auto-Researcher v4

**Resume-worthiness score at start of run: 59 / 100** (rank 6 of 6).

| Signal | Score |
| --- | --- |
| Tech stack prestige (Python + lightweight web UI) | 15 / 25 |
| Commit recency (updated 2026-05-11) | 22 / 25 |
| Feature completeness (single `app/main.py` + `index.html`) | 12 / 20 |
| Stars + visibility | 5 / 15 |
| README quality (6-line snippet on `main`) | 5 / 15 |

### Implemented this run (branch: `claude/brave-bohr-Quaj7`)

No code changes. This commit only seeds the research log on the pre-assigned
branch so the next run has continuity.

### Why no implementation this run

The most obvious open improvements — README overhaul, missing
`.env.example`, missing `LICENSE` — are **already implemented on an
unmerged claude branch**: `claude/brave-bohr-wCHAT` ships the
`docs: overhaul README and add missing .env.example + LICENSE [auto-researcher v4]`
commit. Re-shipping the same content on `claude/brave-bohr-Quaj7` would
violate the "never repeat work already sitting on an open claude/* branch"
guardrail.

The rest of the snPHW next-run list (CI, screenshot, demo recording) needs
a working local Python run to produce confidently — the app surface is just
`app/main.py` + `index.html` + a 213-byte `requirements.txt`, and the
tests/CI shape is not yet verifiable from the file tree alone.

Prioritising the higher-scoring repos (AegisQuant, embodied-skill-composer,
Autonomous-SRE-Agent, plus follow-up polish on FinLens and salesnuero) was
the best use of token budget for this run.

### Next-run candidates (priority order)

1. **Merge `claude/brave-bohr-wCHAT`** — the README rewrite, `.env.example`,
   and LICENSE land in one diff. Highest leverage available.
2. Add `.github/workflows/ci.yml` running `pytest` once the test surface is
   confirmed (none exists in the file tree today).
3. Capture a screenshot of the practice UI rendered from `index.html` for
   inclusion in the new README — single biggest resume signal for a
   web-based interview-prep app.
4. Pin a small smoke test that exercises one mock practice flow without
   calling the LLM provider.

### Prior research-log context

Previous runs (most recent first, none merged to `main`):

- `claude/brave-bohr-snPHW` (2026-04-27) — seeded research log only; no
  code, with the same deferral rationale as this run plus a recommendation
  to do the README rewrite first.
- `claude/brave-bohr-wCHAT` (2026-04-24) — README rewrite, `.env.example`,
  LICENSE. Awaiting merge to `main`.
