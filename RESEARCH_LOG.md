# Research Log

A running log of automated improvement runs against this repo. Each entry documents what was evaluated, what was implemented, and what was deliberately skipped, so future runs avoid repeating work.

## 2026-04-28 — Auto-Researcher v4

**Resume score (start of run):** 57 / 100

- Tech stack prestige: 18 (FastAPI, LangChain, Whisper, WebSockets — solid LLM app stack)
- Commit recency: 17 (pushed 2026-04-14, well within 30 days)
- Feature completeness: 12 (full voice loop, multi-agent pipeline, WebSocket protocol)
- Stars / visibility: 7 (1 star)
- README quality: 3 (only 7 lines pre-run; biggest single gap)

### Implemented on `claude/brave-bohr-jnSqo`

1. **README rewrite**. The previous README was 7 lines and gave no signal about what the project actually does. The new README documents the WebSocket protocol, the multi-agent pipeline, project structure, environment configuration, and a roadmap. This is pure showcase polish — a strong README is the highest-leverage change for a project at 1 star with a thin description.
2. **`.env.example`**. The previous README told users to `cp .env.example .env` but no such file existed. Added one that documents `OPENAI_API_KEY`, optional `OPENAI_MODEL`, `WHISPER_MODEL`, and `LOG_LEVEL`.
3. **This `RESEARCH_LOG.md`**.

### Why these were prioritized

- The README gap was the single largest impact-per-token improvement on this run. The project is feature-complete (PDF → questions → voice eval → summary) but invisible to anyone browsing the repo.
- Adding `.env.example` fixes a broken onboarding instruction that already exists in the README.
- Both changes are zero-risk: documentation and an example file. No code paths are touched.

### Evaluated and skipped this run

- **GitHub Actions CI workflow.** Considered, but the project has no test suite yet, so a CI workflow would either be empty or run lint only. Better to add tests first.
- **Switching to Claude / Anthropic for the agents.** The codebase uses `langchain-openai` consistently. Refactoring the LLM provider mid-run would require touching all three agents and is too risky without local execution. Logged as a next-run candidate.
- **Dockerfile.** Useful but not as high-impact as the README at the current stage.
- **Streaming feedback / multi-language support.** Real features, but require code changes and validation; deferred.

### Next-run candidates

- Add a minimal pytest suite (schemas + document parser) and a GitHub Actions CI workflow.
- Add a Dockerfile + docker-compose for one-command local startup.
- Add an Anthropic / Claude provider option (env-flagged) alongside the existing OpenAI provider, keeping defaults backwards-compatible.
- Wire the declared FAISS dependency into a real retrieval layer (e.g., index a small library of role-specific behavioral questions).
- Persist interview history to SQLite so users can review past sessions.
