# Research Log

This file tracks autonomous research and improvement runs against this repo.
Each run lists what was implemented, what was evaluated and skipped, and the
next-run candidate list.

## 2026-05-15 — Auto-Researcher v4

**Resume-worthiness score at start of run: 61 / 100**

Signal breakdown:
- Tech stack prestige: 14/25 (LLM + Python backend + static HTML frontend)
- Commit recency: 24/25 (last push 2026-05-11)
- Feature completeness: 10/20 (single-page web UI, role-specific practice loop)
- Stars + visibility: 8/15
- README quality: 5/15 (one-line description plus a quick-start snippet)

### Implemented this run

Branch: `claude/brave-bohr-dYRjh`

- `docs(log)`: seeded this RESEARCH_LOG.md.

No functional changes were shipped in this run. The repo has:
- a one-line README,
- no tests directory at root,
- no GitHub Actions workflows,
- a single Python entrypoint (`app/main.py`) and a static `index.html`.

The highest-impact improvements (README rewrite, screenshots, demo GIF,
feature build-out, switch to Claude as the LLM) all require running the
stack first, which would consume billable LLM calls unattended.

### Why no implementation was prioritized

This repo scored lowest (61) of the six targets this run, and the safe
improvements available (e.g. add a placeholder CI workflow) provide little
resume value without a test suite or richer feature surface to anchor them.
A guided run is the right venue for the bigger README + feature work.

### Evaluated and skipped this run

- Major README rewrite with screenshots and demo GIF — skipped: requires running the app.
- Add a backend test suite from scratch — skipped: scope > one unattended run.
- Add a CI workflow — skipped: would have no tests to run, adds little signal.
- Swap to Anthropic Claude as the default LLM — skipped: requires reading and rewriting the prompt path with no regression coverage in place.
- Convert the static `index.html` to a small React or Svelte SPA — skipped: scope too large for one run.

### Next-run candidates

1. Add a minimal mocked test suite around `app/main.py` so future CI has something to run.
2. README rewrite: target role coverage, sample feedback turn, env var reference, screenshot.
3. Anthropic Claude provider with structured rubric output (e.g. STAR coverage, clarity score, communication).
4. Add a `Dockerfile` + `docker compose up` flow for a one-command demo.
5. Persist past sessions to a small SQLite store so users can see progress over time — light feature with strong demo value.
