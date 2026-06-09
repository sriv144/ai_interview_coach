# Research Log

This file tracks autonomous improvements made by the Auto-Researcher agent.
Each entry records what was implemented, what was evaluated and skipped,
and candidates queued for the next run, so we never repeat work.

## 2026-06-09 — Auto-Researcher v4

**Resume-worthiness score at start of run:** 50/100

**Branch:** `claude/brave-bohr-rj6hm9`

### Implemented this run
- `RESEARCH_LOG.md` — seeded only. No code changes shipped this run.

### Why nothing else shipped this run
- The most valuable next change is a README rewrite (current README is ~315 bytes and undersells the project), but the README mentions a `.env.example` that is not in the repo, the `app/` directory hasn't been audited, and there is no visible test suite — so a confident rewrite would mis-describe features or contradict the actual code.
- The right move was to score the repo, queue concrete next-run work, and avoid shipping a low-confidence change on a project that already lags the rest of the portfolio for visibility.

### Evaluated and skipped
- Adding CI — no tests directory was discovered; CI without tests would just run `compileall`, which is cheap polish but doesn't move the resume-worthiness needle.
- Adding `.env.example` — README references it but the actual env vars the backend reads were not verified; risk of shipping a misleading template.
- Auto-generating an expanded README from the README + index.html — high collision risk with the existing project intent.

### Next-run candidates (priority order)
1. **README rewrite** after reading `app/` + `requirements.txt` + `index.html`: add architecture sketch, feature list, screenshot of the web UI, env vars, deployment, model choice (Claude / Anthropic API).
2. **Add `.env.example`** with the exact env vars the backend actually reads.
3. **Add a minimal pytest suite + CI** — even one test (e.g. "app boots, /health returns 200") gives a green badge.
4. **Showcase enhancement**: record a 30-second demo GIF and embed in README. Highest visibility-to-effort ratio.
5. **Claude / Anthropic upgrade**: confirm whether the backend uses `claude-opus-4-8` / `claude-sonnet-4-6` / `claude-haiku-4-5` and surface that in the README so recruiters see the model tier.
