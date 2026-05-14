# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-04-27 — Auto-Researcher v4

**Resume score at start of run:** 43 / 100 — ranked 6 of 6 in the portfolio.

**Branch:** `claude/brave-bohr-snPHW`.

### Implemented this run

No code changes. This commit only seeded the research log so future runs have
memory of what was already evaluated.

### Next-run candidates (priority order)

1. Inventory `app/` source code, then rewrite README with feature list,
   architecture, and a screenshot.
2. Verify or create `.env.example`.
3. Add CI (pytest).
4. Add LICENSE.

## 2026-05-14 — Auto-Researcher v4

**Resume score at start of run:** ~50 / 100 — still last in the portfolio but
the inventory below unlocks most of the previously-blocked polish work.

**Branch:** `claude/brave-bohr-5vVWf`.

### Implemented

- **README rewrite** based on a full inventory of `app/`. The previous README
  was a 6-line snippet that did not name a single feature. The new README
  documents the full WebSocket flow, the Gemini 1.5 Flash question /
  evaluation / summary chain, the local Whisper transcription path, the gTTS
  playback path, the scoring formula, and the WebSocket protocol table. This
  was the explicit #1 next-run candidate from 2026-04-27.
- **`.env.example`:** the previous README referenced `cp .env.example .env`
  but the file did not exist. Added with `GOOGLE_API_KEY` documented.
- **Fixed `requirements.txt`:** the previous file was missing
  `langchain-google-genai`, `google-generativeai`, and `gtts`, which are all
  actually imported at runtime (`app/agents/question_generator.py`,
  `app/agents/answer_evaluator.py`, `app/main.py`). The previous quick-start
  would fail on first run. Added all three.
- **CI workflow** at `.github/workflows/ci.yml`. Byte-compiles `app/` on
  Python 3.11 and 3.12 and verifies all Pydantic schemas import. Skips
  Whisper / torch / faiss in CI to avoid pulling ~1 GB of wheels for what is
  ultimately a smoke check — the schemas-import step still catches breaking
  changes to the WebSocket contract.
- **MIT `LICENSE`.**

### Why this was prioritized

The 2026-04-27 run explicitly punted README rewrite + `.env.example` + CI +
LICENSE pending an inventory of `app/`. That inventory is now done
(question_generator, answer_evaluator, summary_generator, document_parser,
main.py WebSocket loop, schemas.py). Every blocker from last run was
resolvable in this one commit. The requirements-file fix is the most
functionally important change — without `langchain-google-genai` and `gtts`
the documented quick-start was broken.

### Evaluated and skipped

- **Adding actual pytest test cases:** no test directory exists; writing one
  blind risks asserting behavior that does not match real Gemini responses.
  Token budget went to the README/requirements fix instead. Compile + schema
  import in CI is the safe floor.
- **Replacing the module-level `raise ValueError` in
  `question_generator.py`:** raising at import time means `python -c "import
  app.agents.question_generator"` requires a real key. A clean fix is to lazy-
  initialize the Gemini client inside `generate_questions_from_jd`. Deferred
  to a focused refactor PR.
- **Adding a UI screenshot to the README:** would lift signal further, but
  needs a screenshot artifact that this autonomous run cannot generate.

### Next-run candidates

1. Lazy-init Gemini clients in `question_generator.py` and
   `answer_evaluator.py` so the modules can be imported without a live
   `GOOGLE_API_KEY`. Enables real pytest coverage.
2. Add a `tests/` directory with mocked Gemini + Whisper round trips and
   replace the compile-only CI with a pytest CI.
3. Replace the hard-coded `whisper.load_model("base")` with an env-controlled
   model name so CI can run with `tiny.en` while local users keep `base`.
4. README screenshot or short demo GIF of the interview flow.
5. Consider adding an alternate Anthropic Claude backend behind a single
   `LLM_PROVIDER` flag so the project can run end-to-end without a Google key.
