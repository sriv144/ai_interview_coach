# Research Log

Automated improvement log maintained by Auto-Researcher.
Each run appends a dated entry describing what was implemented, what was skipped, and why.

---

## 2026-04-21 — Auto-Researcher v4

**Resume score at the start of this run:** 51/100 (showcase-weak: 5-line README despite working code).

**Implemented (branch `claude/beautiful-einstein-TXG01`):**
- Rewrote `README.md` into a full write-up: architecture, WebSocket flow, scoring rubric (relevance/clarity/impact, 1–10), tech stack, setup, environment variables, WS protocol, project layout, roadmap.
- Added `.env.example` (referenced by the original README but previously missing).
- Seeded this `RESEARCH_LOG.md`.

**Why this was prioritized:**
Code quality was already decent (three-agent pipeline, Pydantic-typed WS messages, final summary), but discoverability was the bottleneck. README length was ~315 bytes with no architecture, no API docs, and no screenshots. "Showcase enhancement mode" per the Auto-Researcher v4 playbook: a great project with a bad README gets no stars.

**Evaluated and skipped this run:**
- CI workflow (pytest): no tests present yet; a CI that only lints would be noise. Deferred until a test suite exists.
- Dockerfile: Whisper model download + torch make images heavy; not a good fit until the model path is parameterized.
- FAISS RAG retrieval: listed in `requirements.txt` but not yet wired. Real feature work, out of scope for a README-focused run.

**Next-run candidates:**
- Add a minimal `pytest` suite around `schemas.py` and `utils/document_parser.py`, then add a GitHub Actions CI workflow.
- Wire FAISS to index a JD-specific corpus of STAR-format interview answers for RAG-backed evaluation.
- Add a `Dockerfile` parameterized by `WHISPER_MODEL`.
- Add a demo GIF or screenshot to the README.
