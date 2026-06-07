# Research Log

Rolling log of autonomous research + improvement passes against this repo.

## 2026-06-07 — Auto-Researcher v4

**Resume score at start of run:** 50 / 100

Breakdown:
- Tech stack prestige: 17 / 25 (multi-agent LLM + WebSocket realtime + audio, but no eye-catching infra)
- Commit recency: 14 / 25
- Feature completeness: 11 / 20 (the pipeline actually works end-to-end)
- Stars + visibility: 2 / 15
- README quality: 6 / 15 (315 bytes — barely existed)

**Why prioritized:** the codebase is significantly more impressive than the README suggested. A multi-agent (question_generator + answer_evaluator + summary_generator) WebSocket-streamed voice interview system was being summarized in 4 lines. That is a pure showcase-enhancement win: high resume impact, near-zero breakage risk because we only touch docs and add metadata files.

**What was implemented (branch `claude/brave-bohr-5OlEN`):**
- `README.md` — complete rewrite. ASCII architecture diagram of the WebSocket + 3-agent pipeline, per-turn flow narrative, feature list, tech-stack table, project structure, quick start, env var pointer, roadmap, contributing, license.
- `.env.example` — first-class env file documenting the LLM key + optional model overrides. Previously the README told users to `cp .env.example .env` but the file did not exist.
- `LICENSE` — MIT, so the repo is actually reusable.
- `.github/workflows/ci.yml` — lint via ruff + a smoke-import of `app.main` on Python 3.10 + 3.11, with the heavy `whisper` import stubbed so CI stays fast and free of torch downloads.
- `RESEARCH_LOG.md` — this file.

### Mid-run correction

First CI run on 3.10 caught a pre-existing inconsistency in this repo:
- `requirements.txt` listed `langchain-openai`, so the initial README + `.env.example` + CI install were written assuming OpenAI.
- The actual code in `app/agents/*` uses Google Gemini (`gemini-1.5-flash-latest`) via `langchain-google-genai` and `google.generativeai`, and `question_generator.py` raises `ValueError` at import time if `GOOGLE_API_KEY` is missing.

Follow-up commit on this same branch fixed all four files:
- `README.md` — provider table + quick start now reference Google Gemini and `GOOGLE_API_KEY` (with the AI Studio link).
- `.env.example` — swapped `OPENAI_API_KEY` for `GOOGLE_API_KEY`, added `GEMINI_MODEL` override.
- `requirements.txt` — removed the unused `langchain-openai`, added `langchain-google-genai`, `google-generativeai`, and `gTTS` (which was being imported but not pinned).
- `.github/workflows/ci.yml` — installs the real Gemini packages (lightweight, no torch), sets `GOOGLE_API_KEY=ci-dummy-key` so the module-level `genai.configure()` call doesn't raise, stubs `whisper.load_model` so torch is never pulled, sets `fail-fast: false` so 3.11 is not cancelled when 3.10 fails.

**What was evaluated and skipped, with reasons:**
- *Migrate LLM calls from Gemini to Anthropic Claude.* High resume value but a real code change touching all three agents; requires re-validating prompt behavior. Deferred — added as an explicit roadmap item.
- *Add a Dockerfile.* Worth doing, but openai-whisper + torch pin makes the image fat and would need real verification. Deferred to a focused pass.
- *Persist interview sessions / add FAISS retrieval over a personal STAR-story corpus.* Listed as roadmap items in the new README; they are real features and need their own design pass, not a drive-by.
- *Add unit tests.* The agent modules call out to LLMs; meaningful tests need mocks for langchain + whisper. Worth doing on a dedicated pass.
- *Fix the existing ruff E402/F401 warnings inside `app/agents/*`.* Behavior change inside the agent files — left for the same focused pass that adds tests.

**Next-run candidates:**
1. Dockerfile + docker-compose with a slim model image.
2. Test suite with mocked LangChain + `whisper.load_model` for each agent.
3. Pluggable LLM provider abstraction so Claude / Gemini / OpenAI can be selected via env var.
4. Persist completed sessions to SQLite so users can review past interviews.
5. Clean up the existing ruff warnings (E402 in `question_generator.py`, F401 in `summary_generator.py`).
