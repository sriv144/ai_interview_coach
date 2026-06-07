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

**Why prioritized:** the codebase is significantly more impressive than the README suggests. A multi-agent (question_generator + answer_evaluator + summary_generator) WebSocket-streamed voice interview system was being summarized in 4 lines. That is a pure showcase-enhancement win: high resume impact, near-zero breakage risk because we only touch docs and add metadata files.

**What was implemented (branch `claude/brave-bohr-5OlEN`):**
- `README.md` — complete rewrite. ASCII architecture diagram of the WebSocket + 3-agent pipeline, per-turn flow narrative, feature list, tech-stack table, project structure, quick start, env var pointer, roadmap, contributing, license.
- `.env.example` — first-class env file documenting LLM key, optional model overrides (`OPENAI_MODEL`, `WHISPER_MODEL`), language, host/port. Previously the README told users to `cp .env.example .env` but the file did not exist.
- `LICENSE` — MIT, so the repo is actually reusable.
- `.github/workflows/ci.yml` — lint via ruff + a smoke-import of `app.main` on Python 3.10 + 3.11, with heavy optional deps (whisper) stubbed so CI stays fast and free of torch downloads.
- `RESEARCH_LOG.md` — this file.

**What was evaluated and skipped, with reasons:**
- *Migrate LLM calls from OpenAI to Anthropic Claude.* High resume value but it is a real code change touching all three agents and requires re-validating prompt behavior. Deferred — would need test coverage before swapping providers.
- *Add a Dockerfile.* Worth doing, but openai-whisper + torch pin makes the image fat and would need real verification. Deferred to a focused pass.
- *Persist interview sessions / add FAISS retrieval over a personal STAR-story corpus.* Listed as roadmap items in the new README; they are real features and need their own design pass, not a drive-by.
- *Add unit tests.* The agent modules call out to LLMs; meaningful tests need mocks for langchain + whisper. Worth doing on a dedicated pass.

**Next-run candidates:**
1. Dockerfile + docker-compose with a slim model image.
2. Test suite with mocked LangChain LLM responses for each agent.
3. Optional: swap to `anthropic` + Claude Sonnet 4 for question generation; benchmark vs. current.
4. Persist completed sessions to SQLite so users can review past interviews.
