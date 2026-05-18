# Research Log

A running log of autonomous research-and-development cycles on ai_interview_coach.

---

## 2026-05-18 — Auto-Researcher v4

**Resume score at start of run:** 48/100
**Branch:** `claude/brave-bohr-9dHiZ`
**Status:** Evaluated, no code change shipped this cycle.

### Why skipped this cycle
- Repo is still at the **initial commit** on `main` (one commit, dated 2026-04-12).
  There is no recent baseline activity to diff against and no contributor signal
  about where the project should evolve next.
- The three top-scoring targets (AegisQuant, embodied-skill-composer,
  Autonomous-SRE-Agent) absorbed the cycle's implementation budget where the
  expected resume impact was higher: a Claude migration (SRE) and a project-polish
  pass plus a benchmark CI workflow.

### Candidates evaluated
- **Claude integration for the coach agent** — high resume value, but needs a deep
  read of the current backend to scope safely; deferred.
- **Frontend polish + screenshots in README** — worth doing but is a multi-step UX
  pass; deferred.
- **CI workflow (pytest + ruff)** — the safest single ship; deferred only because
  the budget went to the top three.

### Next-run candidates
1. Read `src/`, document the actual agent loop, then ship a Claude-backed coach mode.
2. Add `LICENSE`, `CONTRIBUTING.md`, `.github/workflows/ci.yml`, and `RESEARCH_LOG.md`
   updates in one polish commit.
3. Add a `examples/` folder with sample role profiles (SWE, PM, Data, ML).
4. Add screenshots / GIF of the web UI to the README.
5. Voice-mode practice with Anthropic + a TTS provider.
