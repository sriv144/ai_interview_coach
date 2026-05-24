# Research Log

A running log of automated research + improvement passes on this repo.
Each entry records what was implemented, why, what was evaluated but
skipped, and candidate work for the next pass.

## 2026-05-24 — Auto-Researcher v4

**Resume score at start of run:** 39 / 100
*(very thin README, only one commit on `main`, but real working code
underneath — biggest gap is presentation, not capability.)*

**Branch:** `claude/brave-bohr-lJSR8`

**What was implemented**

- Full README rewrite. Documents the WebSocket protocol, architecture,
  feature list, env-var table, project structure, tech stack, and a
  roadmap. The previous README was four lines and hid an already-
  functional FastAPI + LangChain + Whisper + gTTS interview app.
- `.env.example` covering `OPENAI_API_KEY` (required) and optional
  `OPENAI_MODEL`, `WHISPER_MODEL`, `TTS_LANG` overrides.
- Bugfix: added `gtts` to `requirements.txt`. `app/main.py` does
  `from gtts import gTTS`, but `gtts` was not in the dependency list,
  so a clean `pip install -r requirements.txt` would crash on import.
- `.github/workflows/ci.yml`: ruff lint + `compileall` syntax check
  on push to `main` / `claude/**` and on PRs to `main`. Project has
  no tests yet, so CI focuses on guarantees it can keep without false
  positives.

**Why this was prioritised**

The repo has real, non-trivial functionality (PDF JD parsing →
role-specific LLM questions → spoken delivery via gTTS → audio answer
via Whisper → scored evaluation with structured breakdown → end-of-
session summary), but the README is so thin that a casual reader
would assume the project is empty. Showcase-mode polish gives the
largest resume return for the smallest breakage risk — no runtime
behaviour changes except adding a missing dependency, which is itself
a bug fix.

**Evaluated and skipped**

- Adding actual tests: would need to mock OpenAI + Whisper + gTTS
  and the WebSocket lifecycle. Worth doing but is its own focused
  PR and risks chasing flaky audio/network behaviour. Deferred.
- Switching the LLM provider to Anthropic: a real direction (the
  roadmap calls it out), but requires touching all three agents and
  the prompt formats. Not safe as a same-session change without
  manual verification.
- Resume-aware questioning (FAISS is already a dependency): a real
  feature, but multi-file and needs a UI flow for resume upload.
  Logged as a next-run candidate.
- Persisting interview sessions: requires picking a storage layer
  and changing the WebSocket contract. Deferred.

**Next-run candidates**

- Build the resume-aware retrieval path using the existing FAISS
  dependency. Add a second WebSocket step for resume PDF upload,
  index it, and condition `question_generator` on retrieved chunks.
- Add a `tests/` directory with a mocked WebSocket round-trip that
  exercises the JD-parse → question-generate → evaluate → summarise
  loop without calling external APIs.
- Allow the LLM provider to be swapped via env var (`LLM_PROVIDER`)
  with Anthropic + OpenAI back-ends.
- Replace the gTTS dependency with a higher-quality voice (ElevenLabs
  or OpenAI TTS) behind the same abstraction.
- Containerise: add a `Dockerfile` that installs `ffmpeg` so Whisper
  works out of the box.
