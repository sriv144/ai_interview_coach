# Research Log

This file records autonomous improvement runs performed by Auto-Researcher.
Each entry captures what was evaluated, what was implemented, and what was
skipped, so that future runs do not repeat the same work.

## 2026-04-24 — Auto-Researcher v4

**Resume-worthiness score at start of run:** ~50 / 100

Strong technical content under the hood (FastAPI + WebSocket + LangChain +
Whisper + gTTS, real voice interview loop, JD-aware questions) but the public
surface area made the repo look like a stub. The README was 315 bytes, there
was no LICENSE, and `.env.example` was referenced from the README yet missing
from the tree — so every new user hit a failure on first run.

### Implemented on branch `claude/brave-bohr-wCHAT`

- **Full README rewrite.** Added architecture diagram, feature highlights,
  tech stack, quick start, WebSocket protocol reference, project structure,
  env-var table, development notes, and roadmap. This is purely showcase
  polish — no code touched, zero breakage risk.
- **Added `.env.example`.** The old README told users to run
  `cp .env.example .env`, but the file did not exist. Now it does, with
  entries for `GOOGLE_API_KEY`, optional `OPENAI_API_KEY`, `WHISPER_MODEL`,
  and host/port overrides. This is a latent bug fix as much as a docs fix.
- **Added MIT LICENSE.** Previously unlicensed; blocking factor for any
  recruiter or collaborator who takes licensing seriously.
- **Seeded this `RESEARCH_LOG.md`.**

### Why prioritized over alternatives

The repo is feature-complete at the code level — the gap is purely in how it
presents itself. README polish gives the biggest resume-visibility lift per
unit of breakage risk. A broken `.env.example` reference in the quick-start
was the single highest-friction bug a new reader would hit.

### Evaluated and skipped

- **Dockerfile / compose.** Tempting, but Whisper model download and audio
  device assumptions make a generic container brittle. Defer until there is
  a concrete deployment target.
- **pytest harness.** No existing tests, and the code is tightly coupled to
  LLM + audio I/O. Needs a small refactor to inject fakes first; out of
  scope for a docs-focused run.
- **Swap Gemini → Claude.** The constraint is "Claude/Anthropic for any new
  LLM code." Existing Gemini calls are not being touched this run; only new
  code would be on Claude. No new LLM code was added here.
- **FastAPI HTTP endpoints for history.** Listed on the roadmap instead —
  requires a persistence decision (SQLite vs. filesystem JSON).

### Next-run candidates

1. Carve out pure-function seams around the three agents so they can be
   unit-tested with mocked LLM responses.
2. Add an HTTP endpoint `GET /sessions/{id}` that returns the stored
   transcript and evaluations, backed by SQLite.
3. Add a Claude Sonnet backend behind the evaluator as an opt-in toggle.
4. Add screenshots / a short demo GIF to the README (needs a running stack).
5. Dockerfile with Whisper weights pre-baked for a reproducible demo.
