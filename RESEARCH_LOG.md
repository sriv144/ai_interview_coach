# RESEARCH_LOG.md

Persistent memory for the auto-researcher agent. Read top-to-bottom before deciding what to ship on the next pass.

---

## 2026-06-12 — Auto-Researcher v4

**Resume score at start of run:** 51 / 100 (bottom of the 6-repo portfolio)

**Score breakdown:**
- Tech stack prestige: 12/25 — FastAPI + LangChain + Whisper + gTTS is a real-time voice loop, but undersold.
- Commit recency: 22/25 — updated 2026-05-11.
- Feature completeness: 10/20 — backend exists but the surface is opaque to a visitor.
- Stars / visibility: 3/15 — 1 star.
- README quality: 4/15 — **315 bytes** for a multi-agent WebSocket voice interview system. The single biggest leverage point in the entire portfolio.

### What was implemented this pass (branch `claude/brave-bohr-qiarsa`)

- `RESEARCH_LOG.md` — this file. Log-only commit.

### Why no code this pass

This repo is the most-saturated by prior auto-researcher work in the entire portfolio: PRs #2–#13 every single one is a README rewrite, `.env.example`, LICENSE, CI workflow, or requirements.txt repair. Twelve consecutive passes have shipped variations on the same docs-hygiene change without any landing on `main`. Stacking PR #14 in that pile is anti-impact.

The correct move for this repo is **either** (a) the maintainer merges one of the existing PRs and resets the cycle, **or** (b) a future pass ships a genuine new feature — not another README rewrite — that the existing scaffolding PRs would compose against.

### Evaluated and skipped

- **Another README rewrite** — would be PR rewrite #11. No.
- **Yet another `.env.example`** — already in PRs #2, #3, #4, #5, #6, #7, #8, #9. No.
- **Yet another CI workflow** — already in PRs #2, #5, #6, #8, #9. No.
- **A real new feature** — high impact but requires reading `app/main.py`, `app/agents/*`, the WebSocket protocol, and the existing schemas in detail. Out of scope for an atomic commit.

### Next-run candidates (priority order)

1. **Maintainer hygiene first**: pick one of the open scaffolding PRs (suggest PR #9, which is the most complete: README + LICENSE + `.env.example` + CI) and merge it. This unblocks every subsequent pass.
2. **Real feature — Anthropic Claude rubric-scoring endpoint**: add a `POST /api/v1/score` route that takes `(question, answer, role)` and returns a structured Claude-scored rubric (clarity / depth / STAR-method coverage / technical accuracy). Useful, new capability, surfaces Claude as the LLM backbone, and gives the README something concrete to demo.
3. **Tests/ directory**: any baseline coverage on `app/agents/*` would unblock the CI workflow PRs.
4. **Demo screenshot / GIF** of the WebSocket voice loop, embedded in the (already-rewritten) README.
5. **Dockerfile + docker-compose** so the `cp .env.example .env && uvicorn ...` quickstart becomes `docker compose up`.
