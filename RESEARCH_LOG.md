# Research Log

This log tracks autonomous-research / auto-improvement passes over the
repository. Each section records what was scored, what was implemented,
and what was deliberately skipped, so future runs can avoid re-doing
work that has already shipped.

## 2026-06-02 — Auto-Researcher v4

### Resume-worthiness score at start of run

`53 / 100`

Breakdown (out of 100, see auto-researcher rubric):

- Tech stack prestige: 16 / 25 — FastAPI + LangChain + Whisper + gTTS is
  a respectable real-time voice AI stack but not as differentiated as
  multi-agent / RL / distributed work.
- Commit recency: 17 / 25 — The repo is recent but quiet.
- Feature completeness: 10 / 20 — The backend WebSocket flow is
  actually quite complete (generation → scoring → final summary), but
  the lack of docs hid that fact.
- Stars / visibility: 6 / 15.
- README quality: 4 / 15 — The previous README was six lines.

### Implemented on branch `claude/brave-bohr-MN9a4`

- **docs: full README overhaul.** Documents the WebSocket protocol
  (binary JD upload, question / evaluation / final_summary frames),
  Pydantic schemas, module map, environment variables, troubleshooting,
  and roadmap. Highest ROI improvement on the repo — the underlying
  app is genuinely impressive once the docs surface it.
- **fix: add missing `gtts` to `requirements.txt`.** `app/main.py`
  imports `gtts` to synthesize the spoken questions, but `gtts` was
  not listed in `requirements.txt`. A fresh install would crash on
  the first WebSocket connection. This is a real bug fix, not just
  polish.
- **docs: add `.env.example`.** The README told users to
  `cp .env.example .env`, but the template file did not exist. Now it
  does, with `OPENAI_API_KEY` and optional `OPENAI_MODEL`,
  `WHISPER_MODEL`, `HOST`, `PORT` entries.
- **ci: add `.github/workflows/ci.yml`.** Runs syntax / import
  smoke-tests on Python 3.10–3.12 so the missing-import class of
  regression that this commit fixes cannot silently re-appear.
- **docs: seed this `RESEARCH_LOG.md`.**

### Evaluated and skipped

- Rewriting the LangChain agents to use Claude / `langchain-anthropic`
  instead of OpenAI. Skipped this run because it changes runtime
  behavior and prompt contracts that the existing agents depend on,
  and there are no tests yet to guard the migration. Queued for a
  future run after tests are added.
- Adding a real test suite under `tests/`. Skipped because the
  agents make external LLM calls that need careful mocking; doing
  it sloppily is worse than not doing it. Queued.
- Dockerfile + Compose stack. Skipped to keep this commit focused;
  README roadmap calls it out.

### Candidates for next run

1. Add a `tests/` package with mocked LangChain + Whisper to lock in
   the WebSocket contract and the Pydantic response schemas.
2. Migrate the LLM provider to Claude (`langchain-anthropic`,
   `ANTHROPIC_API_KEY`) with a provider-selector environment variable.
3. Add screenshots / a short GIF of a live interview session to the
   README so visitors see the product without cloning.
4. Persist session history (SQLite) so users can review past attempts.
5. Dockerfile + `docker-compose.yaml` for a one-command launch.
