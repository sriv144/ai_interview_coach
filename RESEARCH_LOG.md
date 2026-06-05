# Research Log

This file tracks Auto-Researcher passes against this repository: what was
implemented, what was evaluated and skipped, and what is queued for next run.

## 2026-06-05 — Auto-Researcher v4

**Resume score at start of run:** 39 / 100

Lowest score of the six target repos, but the highest-leverage showcase fix.
The code under `app/` is a real-time WebSocket interview pipeline (FastAPI +
LangChain + Whisper + gTTS), but the public-facing surface was a 315-byte
README with no LICENSE, no `.env.example`, and no CI — so reviewers would
bounce before they ever ran it.

### Implemented (branch `claude/brave-bohr-eZfYm`)

- `README.md` rewritten end-to-end: positioning, feature list, ASCII
  architecture diagram of the `/ws/interview` flow, env table, tech stack,
  repo map, roadmap, badges.
- `.env.example` documenting `OPENAI_API_KEY` and `WHISPER_MODEL` so the
  README quickstart is reproducible.
- `LICENSE` (MIT) so the repo is legally usable and forkable.
- `.github/workflows/ci.yml`: ruff `E9,F63,F7,F82` lint over `app/` — picks
  up syntax and undefined-name bugs without forcing a style overhaul.

### Why this was prioritized

Readme quality and CI signals are the cheapest, most visible resume wins:
any recruiter or interviewer skimming the repo lands on the README first,
and a green CI badge is a low-cost trust signal. The underlying code was
already interesting (multi-agent LangChain orchestrating Whisper + gTTS
over a single WebSocket), so all the documentation needed was a clear
write-up of what already works.

### Evaluated and skipped

- **Add an Anthropic LLM provider option.** Touches every agent in
  `app/agents/` (question_generator, answer_evaluator, summary_generator)
  and changes their prompt contracts. High value but non-trivial; deferred
  to its own focused branch where it can be reviewed and tested in isolation.
- **Dockerfile + docker-compose.** Whisper pulls heavy native deps (ffmpeg,
  torch); a half-baked image risks shipping a broken build. Punt until the
  provider abstraction lets us slim the runtime image.
- **Persistent interview history.** Needs a storage decision (sqlite vs
  external) plus a migration story. Skipped for now — the WebSocket flow is
  stateless today and the README acknowledges that.

### Candidates for next run

1. Add an Anthropic provider behind a `LLM_PROVIDER` env var; default to
   OpenAI for back-compat.
2. Ship a Dockerfile with ffmpeg baked in plus a `docker-compose.yml`.
3. Replace `print(...)` debug logging in `app/main.py` with structured
   `logging` calls so production deployments stay grep-friendly.
4. Add a `/healthz` endpoint for container orchestrators.
5. Persist interview history to sqlite under a `history/` route.
