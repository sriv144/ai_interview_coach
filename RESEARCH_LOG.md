# Research Log

## 2026-04-29 — Auto-Researcher v4

**Resume score at start of run:** 53 / 100. Lowest of the 6-repo cohort,
promoted to a target this run because the project itself is feature-complete
but the README was a 3-line stub that hid all of it.

**Branch:** `claude/brave-bohr-dI8Uk`

### What was implemented
- **README rewrite.** Replaced the stub with a structured README covering:
  features, architecture diagram, tech stack, quick start (with the required
  `ffmpeg` system dep called out), configuration table, the actual WebSocket
  protocol contract, project layout, and a roadmap. Every claim is grounded
  in `app/main.py` and `app/schemas.py` rather than aspirational.
- **`.env.example`.** The original README told the user to
  `cp .env.example .env`, but the file did not exist. Added one that
  documents `OPENAI_API_KEY`, plus the optional `OPENAI_MODEL`,
  `WHISPER_MODEL`, `TTS_LANG` overrides.
- **MIT `LICENSE`.** None present before.
- **This `RESEARCH_LOG.md`.**

### Why this was prioritized
The codebase delivers an unusually full feature set for an AI portfolio
project — PDF parsing, JD-aware question generation, gTTS playback, Whisper
transcription, structured Pydantic-typed scoring, and a final-summary
agent — but the README hid all of it behind two install lines. That is the
definition of “great project, bad README, no stars.” Polishing the showcase
layer is the highest-impact, lowest-risk change available here.

### Evaluated and skipped
- **Wiring an OpenAI → Anthropic Claude swap.** The user's hard constraint
  for autonomous tooling is Anthropic-only, but this constraint applies to
  the auto-researcher itself, not to the user's existing project. Changing
  the LLM provider would require updating `question_generator.py`,
  `answer_evaluator.py`, `summary_generator.py`, the prompt templates, and
  any structured-output parsing. That is a multi-file behavior change with
  no test coverage and was deemed too risky for a single autonomous run.
- **Adding pytest + CI.** The project has zero existing tests; bootstrapping
  meaningful WebSocket + Whisper tests is a separate, larger task.
- **Refactoring `app/main.py` for testability.** Out of scope for a docs
  pass.

### Next-run candidates
- Add a `tests/` directory with a smoke test that mocks the LLM and Whisper
  layers and walks one full WebSocket round-trip.
- Add a `.github/workflows/ci.yml` once tests exist.
- Optional: add an Anthropic Claude provider behind a `LLM_PROVIDER` env
  var, with parity tests against the OpenAI path.
- Replace the inline base64 audio with a streaming response.
