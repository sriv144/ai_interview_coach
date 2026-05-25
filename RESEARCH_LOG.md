# Research Log

A running record of auto-researcher passes against this repo. Each entry
lists the resume score at the start of the run, what was implemented and
why, and what was evaluated and skipped so future passes don't repeat the
same analysis.

## 2026-05-25 -- Auto-Researcher v4

**Resume score at start:** 50/100. Tech stack is decent (FastAPI + Gemini
+ Whisper + LangChain) and the underlying app is substantive, but the
README was 315 bytes, there was no `.env.example`, no LICENSE, no CI, and
`requirements.txt` was wrong (listed `langchain-openai` while the code
imports `langchain-google-genai` + `google-generativeai` + `gtts`). A
fresh clone would crash at first import.

**Implemented on branch `claude/brave-bohr-FVAfQ`:**

- Rewrote `requirements.txt` to match the actual imports in
  `app/agents/*` and `app/main.py`: added `langchain-google-genai`,
  `google-generativeai`, `gTTS`, `websockets`, `pydantic`; dropped the
  unused `langchain-openai`; loosened pins to compatible ranges.
- Added `.env.example` documenting `GOOGLE_API_KEY` (the only required
  secret) plus optional overrides.
- Replaced the stub README with a real one: architecture diagram, project
  layout, ffmpeg/Whisper system deps, scoring formula derived from
  `answer_evaluator.py`, configuration table, and a troubleshooting
  section keyed off the exact errors a broken `requirements.txt` produces.
- Added MIT `LICENSE`.
- Added `.github/workflows/ci.yml`: installs ffmpeg + deps, runs
  `compileall`, and does an import smoke test so requirements drift fails
  CI rather than first-run users.

**Why this was prioritized:** The bug in `requirements.txt` was a blocking
defect for any new user. Combined with the 315-byte README it meant the
project scored poorly on showcase value despite having real substance.
Fixing both unlocks the most resume value per byte changed.

**Evaluated and skipped:**

- Swapping Gemini for Anthropic Claude: cross-cutting refactor across
  three agents + schemas. Higher risk of regressing the working
  scoring/summary behavior. Better as a dedicated future pass that adds a
  provider abstraction.
- Adding pytest coverage: there are no existing tests and the agents make
  live network calls, so meaningful tests need mocking infrastructure
  that's larger than this pass.
- Dockerizing: Whisper's model download + ffmpeg layer makes the image
  large; deferring until there's a deployment target that actually needs
  it.

**Next-run candidates:**

- Provider abstraction: pluggable LLM backend (Gemini today, Claude or
  GPT tomorrow) behind a single interface.
- Persist sessions to a small SQLite store so a candidate can resume.
- Add a server-side rate limit on `/ws/interview` (currently unbounded).
- Vitest/Playwright smoke test of `index.html` against a mocked server.
