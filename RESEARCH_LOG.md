# AI Interview Coach — Auto-Researcher Log

A cumulative record of automated research + implementation passes on this
repository. Each entry captures what was evaluated, what shipped, and what
was deferred so that future runs avoid duplicating work.

## 2026-06-10 — Auto-Researcher v4

**Resume-worthiness score at start of run:** 60 / 100
(tech 12, recency 22, completeness 11, stars 11, README 4)

**Branch:** `claude/brave-bohr-0tcsmd`

### Implemented

- Seeded this `RESEARCH_LOG.md` so future automated passes can avoid
  duplicating work.

### Why this repo was not selected for code changes this run

ai_interview_coach placed last of the six target repos on
resume-worthiness. The repo's README is only 315 bytes and there is no
`tests/` directory, so the most valuable next step is content + a real
feature, not scaffolding. That work is too large to ship safely inside
a single atomic commit during a batched auto-researcher pass; it needs
its own focused run.

### Evaluated and deliberately deferred

- **Full `README.md` rewrite** — motivation, screenshot, features,
  setup, API contract, roadmap. The current README does not tell an
  interviewer what the project actually does.
- **A real `.env.example`** with Anthropic key, model name, port, and
  any TTS / STT provider keys the app may use.
- **Baseline `tests/`** — a smoke test against the FastAPI / Flask
  surface in `app/`, then a CI workflow once tests exist.
- **Anthropic Claude scoring rubric module** — the natural next
  feature (interview answer grading with structured rubric output via
  Claude's tool-use API).
- **Web UI screenshot** added to README to lift the visual signal.

### Next-run candidates (priority order)

1. Rewrite `README.md` with sections: What it does, Screenshot, Setup,
   Architecture, API, Roadmap.
2. Write `.env.example` after reading `app/` to enumerate required
   environment variables.
3. Add a `tests/` directory with a single happy-path test against the
   web entrypoint.
4. Implement an Anthropic Claude rubric-scoring endpoint as the
   flagship feature.
5. Add a CI workflow once tests exist.
