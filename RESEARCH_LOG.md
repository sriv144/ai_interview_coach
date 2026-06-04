# Research Log

Long-running notebook for the auto-researcher: what was evaluated, what was
shipped, and what is queued for next runs.

## 2026-06-04 - Auto-Researcher v4

**Resume score going in:** 52 / 100

Lowest-scoring repo in the portfolio. README was effectively empty (5 lines)
and the project did not actually install from a clean checkout, which is the
worst signal a reviewer can pick up from a public repo.

### Implemented (branch: claude/brave-bohr-ahxvL)

- **fix: align requirements.txt with actual imports.**
  The code imports `langchain_google_genai`, `google.generativeai`,
  `PyPDF2`, and `gtts`. The old requirements.txt listed
  `langchain-openai`, `pypdf`, and omitted `gTTS` entirely, so
  `pip install -r requirements.txt && python -m uvicorn app.main:app`
  would fail at import time. Updated requirements.txt to match the
  real surface area.
- **docs: real README.** Rewrote the README from 5 lines to a complete
  reference: architecture diagram, feature list, project layout,
  WebSocket protocol table, setup, and roadmap.
- **chore: add .env.example.** The agents raise `ValueError` if
  `GOOGLE_API_KEY` is missing; new contributors had no signal that this
  was required. Added a documented `.env.example`.

### Why this was prioritized

- Highest delta-per-token on the whole portfolio: a broken install + an
  empty README is the cheapest thing to fix and the most damaging thing
  to leave alone for a public, resume-linked repo.
- All three changes are docs / metadata / dependency-pin work. No
  application logic was touched, so the runtime risk is essentially
  zero.

### Evaluated and skipped

- **Anthropic Claude backend.** Considered swapping Gemini for Claude
  to satisfy the "Anthropic models only" preference for new LLM code.
  Skipped this run: the existing agents are tightly bound to
  `ChatGoogleGenerativeAI` and the Pydantic output-parser prompts are
  tuned for Gemini. A safe swap is a multi-file refactor with its own
  test plan, not a low-risk fix.
- **Add a pytest suite.** No tests exist today. Queued for a follow-up
  run; needs Whisper / Gemini stubs to be hermetic in CI.
- **GitHub Actions CI.** Deferred until there are tests worth running.

### Next-run candidates

1. Add a minimal pytest suite around `document_parser` and the Pydantic
   schemas (no network).
2. Introduce an `LLMClient` abstraction so a Claude backend can be added
   alongside Gemini behind an env switch.
3. Persist sessions to SQLite so candidates can review history.
4. Add streaming ASR so the candidate gets per-token feedback instead of
   waiting for Whisper to finish.
