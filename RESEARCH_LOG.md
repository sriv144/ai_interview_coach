# Research Log

A running ledger of autonomous-improvement passes against this repository.
Each entry records the resume-worthiness score at the start of the run,
what was implemented, what was evaluated and skipped, and the next-run
candidate list.

## 2026-05-19 — Auto-Researcher v4

**Resume-worthiness score at start of run: 62 / 100** (rank 6 of 6).

| Signal | Score |
| --- | --- |
| Tech stack prestige (LLM + WebSockets + Whisper + gTTS + LangChain) | 15 / 25 |
| Commit recency (updated 2026-05-11) | 22 / 25 |
| Feature completeness (WebSocket interview loop, 3-agent prompts, voice IO) | 15 / 20 |
| Stars + visibility (1 star) | 4 / 15 |
| README quality (6-line stub on `main`; richer rewrites on sibling claude branches) | 6 / 15 |

### Implemented this run (branch: `claude/brave-bohr-lpd1a`)

No code or config changes. This commit only seeds `RESEARCH_LOG.md` on
the pre-assigned branch so the next run has continuity.

### Why no implementation this run

The highest-leverage open improvements on this repo — README rewrite,
missing `.env.example`, missing LICENSE, missing `gTTS` runtime
dependency — are **already implemented on multiple unmerged
`claude/brave-bohr-*` branches**:

- `dI8Uk` (2026-04-29) — full README rewrite + `.env.example` + MIT
  LICENSE grounded in `app/main.py` / `app/schemas.py`.
- `Ow84F` (2026-05-16) — full README rewrite + `.env.example` + adds
  missing `gTTS` to `requirements.txt` (a latent ImportError on first
  fresh install).
- `wCHAT` (2026-04-24) — README overhaul + `.env.example` + LICENSE.

Shipping any of these again on `lpd1a` would just be a fifth duplicate.
The remaining open work (pytest smoke test through the WebSocket loop,
Docker / docker-compose, Anthropic Claude swap of the three LangChain
agents) all require running the actual stack locally to verify, since
the project has zero existing tests and is tightly coupled to LLM +
Whisper + audio IO.

Token budget this run went to the three repos with clear, unblocked,
low-risk next-run candidates:

- `FinLens` — Anthropic Claude provider option behind `LLM_PROVIDER`
  (`claude/admiring-davinci-lpd1a`).
- `Autonomous-SRE-Agent` — helm lint + docker compose validation
  workflow (`claude/fervent-edison-lpd1a`).
- `salesnuero` — first CI workflow on the repo, backend compile +
  frontend build (`claude/compassionate-keller-lpd1a`).

### Evaluated and skipped

- **`tests/test_websocket_smoke.py`** with a mocked LLM + mocked
  Whisper exercising one full round-trip through `app/main.py`. Real
  value, but needs `httpx.ASGITransport` set up against the FastAPI app
  plus careful stubs of `OpenAI`, `gTTS`, and `whisper.load_model` —
  too many moving parts for a safe one-shot.
- **`.github/workflows/ci.yml`** running `pytest`. Blocked on the test
  smoke above; a CI gate with no tests is theater.
- **`Dockerfile` + `docker-compose.yml`.** `openai-whisper` weights are
  large and a non-trivial multi-stage build is needed to keep the image
  reasonable; better as its own focused PR.
- **Anthropic Claude swap of `question_generator.py`,
  `answer_evaluator.py`, `summary_generator.py`.** Aligns with the
  portfolio direction (FinLens already shipped its Claude provider this
  run) but touches three agent modules + prompt templates with no test
  coverage to catch regressions — needs its own branch with parity tests.
- **Promoting `claude/brave-bohr-wCHAT` (or `dI8Uk`, or `Ow84F`) to
  `main`.** That is the actual highest-leverage action available; it is
  an owner decision, not an autonomous one.

### Next-run candidates (priority order)

1. **Merge one of `wCHAT` / `dI8Uk` / `Ow84F`** so the README rewrite,
   `.env.example`, LICENSE, and `gTTS` dep fix land on `main`. After
   that, the resume score jumps roughly 10 points without writing a
   single new line of code.
2. Add `tests/test_websocket_smoke.py` with mocked LLM + mocked Whisper
   exercising one full WebSocket round-trip.
3. Add `.github/workflows/ci.yml` running `pytest` once (2) lands.
4. Capture a screenshot of the practice UI rendered from `index.html`
   for inclusion in the merged README — single biggest resume signal
   for a web-based interview-prep app.
5. Port the three LangChain agents to `langchain-anthropic` so the
   project actually runs on Claude, mirroring the FinLens
   `LLM_PROVIDER` pattern.

### Prior research-log context

Previous runs on unmerged `claude/brave-bohr-*` branches (most recent
first, none merged to `main`):

- `Quaj7` (2026-05-17) — seeded log only; no code (same deferral
  rationale as this run).
- `Ow84F` (2026-05-16) — README rewrite + `.env.example` + `gTTS` dep fix.
- `dI8Uk` (2026-04-29) — README rewrite + `.env.example` + MIT LICENSE.
- `snPHW` (2026-04-27) — seeded log only; no code.
- `wCHAT` (2026-04-24) — README overhaul + `.env.example` + LICENSE.
