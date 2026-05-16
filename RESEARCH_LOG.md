# Research Log

A running log of automated research-and-development passes against this repository.

## 2026-05-16 — Auto-Researcher v4

**Resume-worthiness score at start of run: 51 / 100**

| Signal | Score |
| --- | --- |
| Tech stack prestige (LLM + WebSockets + Whisper + gTTS) | 15 / 25 |
| Commit recency (updated 2026-05-11) | 22 / 25 |
| Feature completeness (working WebSocket interview loop, multi-agent prompts, voice IO) | 14 / 20 |
| Stars + visibility (1 star) | 3 / 15 |
| README quality (315-byte README before this run) | 3 / 15 |

### Implemented this run (branch: `claude/brave-bohr-Ow84F`)

- **docs: full README rewrite.** Expanded the 315-byte README into a complete showcase doc with feature list, tech stack, project structure, environment variables, interview flow, and roadmap. This is the showcase enhancement of the run — the project itself is far more impressive than its previous README suggested.
- **feat: seed `.env.example`.** The previous README told users to `cp .env.example .env`, but the file did not exist. Added a template that documents the required `OPENAI_API_KEY`.
- **fix: add missing `gTTS` runtime dependency.** `app/main.py` imports `from gtts import gTTS` but the package was not declared in `requirements.txt`, so a fresh `pip install -r requirements.txt` would `ImportError` on the first WebSocket request. Added `gTTS` to the dependency list.

### Why this was prioritized

ai_interview_coach scored lowest on README quality (3/15) of the 6 target repos despite having a real working backend — a WebSocket interview loop, three LangChain agents, and audio in/out. A repo that *is* better than it *looks* leaks the most opportunity per token of effort, so a documentation pass is by far the cheapest way to raise its perceived quality. The missing `.env.example` and missing `gTTS` dependency were genuine bugs uncovered while writing the README and would block any new contributor on first install.

### Evaluated and skipped

- **Dockerfile + docker-compose.** Would be a useful next addition, but the app pulls `openai-whisper` (large) and a meaningful Dockerfile would need a multi-stage build to keep the image reasonable. Out of scope for a safe single-commit pass.
- **Anthropic / Claude swap of the LangChain pipelines.** High-value refactor and aligns with the broader portfolio direction, but touches all three agent modules and changes runtime behaviour. Deserves its own dedicated branch.
- **Frontend cleanup.** The static `index.html` is reasonable; visible UX work needs browser testing that an autonomous run cannot do.

### Next-run candidates

1. Port the three LangChain agents to `langchain-anthropic` so the project actually runs on Claude.
2. Add a pytest layer around `schemas.py` and the WebSocket protocol (`fastapi.testclient`), wired into a GitHub Actions CI workflow.
3. Add a Dockerfile for one-command local deploy.
4. Persist interview sessions (SQLite or JSON) so candidates can revisit past feedback.
