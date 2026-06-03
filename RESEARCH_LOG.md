# Research Log

Autonomous research-agent activity log for ai_interview_coach.

Each entry records: (a) what was implemented, (b) why it was
prioritized, (c) what was evaluated but skipped, and (d) next-run
candidates. Do not delete prior entries.

---

## 2026-06-03 — Auto-Researcher v4

**Resume-worthiness score at start of run:** 53 / 100

- Stack prestige (25): 16 — FastAPI + WebSocket + LangChain +
  Whisper + Gemini agents is a respectable AI/LLM stack but not
  RL/infra-tier.
- Commit recency (25): 18 — 23 days since last push.
- Feature completeness (20): 12 — the WebSocket interview loop,
  3 LangChain agents (question generator, answer evaluator, final
  summary), Whisper STT, gTTS audio out are all wired and working.
- Stars / visibility (15): 4 — 1 star, public topics.
- README quality (15): 3 — a single four-line `Quick start` block.
  This was the dominant defect of the repo.

### Implemented on `claude/brave-bohr-oCTQH`

1. **Full README rewrite.** New sections: how it works (with an
   ASCII data-flow diagram), stack table, project layout tree,
   quick-start (cross-platform, including the ffmpeg dep that
   Whisper requires), environment variables table, the actual
   WebSocket protocol the browser must speak, local-dev steps,
   roadmap.
2. **`.env.example`.** The agents fail-fast on a missing
   `GOOGLE_API_KEY` (`question_generator.py` raises at import), so
   a documented template was a hard prerequisite for a working
   first-run.
3. **`.github/workflows/ci.yml`.** Python 3.11 + 3.12 matrix,
   installs `ffmpeg` + project deps, runs `ruff check` (non-
   blocking) and `compileall` over `app/`. Dummy `GOOGLE_API_KEY`
   in env so the import-time check in the agents does not crash CI.

All three files landed in a single atomic commit, including the
seeded `RESEARCH_LOG.md`.

### Why these were prioritized

The code under `app/` is genuinely sophisticated (typed Pydantic
WebSocket protocol, three composed LangChain agents, real audio
in / audio out, final scoring summary). But the README hid all of
it — a recruiter visiting the repo saw four lines of bullet points.
Rewriting the README is the single highest-leverage move and is
zero-risk to runtime behavior.

### Evaluated and skipped

- **Move Whisper to a faster backend (faster-whisper / mlx-whisper).**
  Real win, but would require refactoring `answer_evaluator.py` and
  testing on audio fixtures we don't have. Defer.
- **Add a Dockerfile.** Listed in the roadmap; would also need a
  ffmpeg base image. Defer.
- **Swap Gemini for Anthropic Claude.** Possible (the LangChain
  chain is trivially provider-agnostic) but would change the public
  behavior of the project and break anyone with a `GOOGLE_API_KEY`
  already set. The README now documents the OpenAI fallback path
  and the next-run plan adds Anthropic alongside.
- **Real pytest suite.** The repo has no `tests/` directory yet;
  building one needs fixture audio + JD PDFs. Defer.

### Next-run candidates

1. Add an Anthropic Claude agent backend alongside Gemini, exposed
   via an `LLM_PROVIDER` env var, defaulting to Gemini for back-
   compat.
2. Build a minimal `tests/` suite that mocks the LLM calls and
   tests the WebSocket state machine.
3. Add a Dockerfile + docker-compose so the app launches with one
   command, including ffmpeg.
4. Persist session history to disk so the candidate can resume.
5. Live-update the score breakdown in the front-end during the
   interview.
