# Research Log

This log tracks autonomous-research improvements applied to this repository.
Each run records what was implemented, what was considered and skipped, and
what the next candidate improvements are. Do not delete entries; append new ones.

## 2026-06-01 — Auto-Researcher v4

**Resume-worthiness score at start of run:** ~30 / 100

The codebase is genuinely solid (FastAPI + WebSocket interview loop, Whisper STT,
gTTS TTS, LangChain question/evaluation/summary agents, fully typed via Pydantic),
but the README was 315 bytes and a single Quick Start block. None of the core
features were surfaced — a recruiter looking at the front page would have no
idea this project exists at the level it does.

### What was implemented

Branch: `claude/brave-bohr-nPZT4`

- **`README.md`** — full rewrite. Added a why-it-exists framing, a feature list
  grounded in the actual code (`app/agents/*`, `app/schemas.py`, the
  `/ws/interview` WebSocket loop), an ASCII architecture diagram, a tech-stack
  table, project layout, an explicit end-to-end flow describing every
  WebSocket message type, the scoring rubric, an env-var reference, and a
  roadmap. Total length ≈ 6.5 KB — same project, professionally surfaced.
- **`.env.example`** — created. Documents `OPENAI_API_KEY` (the only required
  value) plus optional knobs for model id, temperature, Whisper model size,
  host/port, and log level. Matches the variables actually referenced from
  the code today.
- **`RESEARCH_LOG.md`** — seeded (this file).

### Why this was prioritized

Classic showcase-enhancement case: the project is more impressive than it
looks. Improving the README has the highest resume impact-per-LOC of anything
on this repo, with effectively zero risk of breaking anything — docs only.
Adding `.env.example` removes a real onboarding papercut (the old README
referred to `.env.example` even though it didn't exist).

### What was evaluated and skipped

- **CI workflow (pytest + ruff).** Skipped this run — the repo has no `tests/`
  directory yet, so a CI job would either be empty or false-green. Better to
  land tests first, then wire CI. Logged as a next-run candidate.
- **LICENSE file.** Skipped — license choice is the owner's call, not the
  agent's; flagging in the roadmap is enough.
- **Refactor the WebSocket loop into smaller handlers.** Skipped — working
  code, low risk if untouched, no failing test to anchor a refactor.
- **Swap gTTS for a streaming TTS.** High-impact feature but multi-file and
  needs design choices (Eleven Labs? Azure? local Piper?). Out of scope for a
  safe atomic commit; left in the roadmap.
- **Migrate LangChain LLM to Anthropic Claude.** The auto-researcher's own
  constraint is Claude-only, but this is a user-owned product choice in an
  OSS repo and a behaviour-changing edit. Not safe to ship in a doc-polish
  commit; flagged for a future, focused PR.

### Next-run candidates

1. Add a minimal pytest suite covering `schemas.py` (Pydantic round-trip),
   `utils/document_parser.py`, and a mocked agent call, then wire a GitHub
   Actions CI workflow.
2. Add an `Anthropic / Claude` provider option behind an env-var switch so
   the LLM backend is pluggable (matches the auto-researcher's own model
   policy without breaking existing OpenAI users).
3. Add a `Dockerfile` and `docker-compose.yml` so the project can be brought
   up with one command (currently requires a venv + Whisper model download).
4. Capture a short demo GIF (record one end-to-end interview) and embed it
   at the top of the README. Demo media is consistently the single biggest
   star/visit driver for projects in this category.
