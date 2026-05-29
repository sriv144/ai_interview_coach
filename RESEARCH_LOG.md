# Research Log

Automated improvement history for this repository, maintained by the
Auto-Researcher agent.

## 2026-05-29 — Auto-Researcher v4

**Resume-worthiness score at start of run: 55 / 100**
(tech stack 15 · commit recency 24 · feature completeness 11 · stars 3 · README 2)

### Implemented (branch `claude/brave-bohr-facaX`)
- **Fixed a broken dependency manifest.** `app/main.py` and the three agents
  import `langchain_google_genai`, `google.generativeai` and `gTTS`, and require
  a `GOOGLE_API_KEY`, but `requirements.txt` listed `langchain-openai` and
  omitted `gTTS` and `google-generativeai`. A clean clone therefore failed at
  import. Added the real dependencies and removed the unused `langchain-openai`.
- **Added `.env.example`** with `GOOGLE_API_KEY` — the previous README told users
  to `cp .env.example .env`, but the file did not exist.
- **Rewrote the README** (was ~5 lines) into a full showcase: feature list, a
  request-flow diagram, tech-stack table, prerequisites (including the required
  `ffmpeg` for Whisper), accurate setup, the correct `uvicorn app.main:app` run
  command, and a project-structure map.

### Why this was prioritized
This is a genuinely feature-rich project (FastAPI WebSocket interview loop with
Gemini question generation, Whisper transcription, gTTS audio, and structured
scoring) hidden behind near-empty docs and an install that did not work out of
the box — the textbook "great project, no stars" case. Repairing the manifest
restores a working clone, and a strong README is the highest-leverage,
zero-risk way to raise the repo's resume value. No application logic was
changed.

### Evaluated and skipped
- **Adding tests + CI** — there are no tests yet, and a meaningful suite needs
  mocking of the Gemini and Whisper calls; larger scope, deferred to a future
  run.
- **Refactoring the run path** (`main.py` has no `__main__` server entry) — left
  the code untouched and documented the correct `uvicorn` invocation instead, to
  avoid changing behavior.

### Next-run candidates
- Add a pytest suite with mocked Gemini / Whisper and a CI workflow.
- Add screenshots or a short demo GIF of the interview UI.
- Add a Dockerfile that bundles ffmpeg for one-command setup.
- Pin dependency versions for reproducible installs.
