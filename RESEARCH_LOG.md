# Research Log — AI Interview Coach

Durable memory for the auto-researcher agent. Each run appends an entry
documenting what was implemented, what was deliberately skipped, and the
next viable improvement. Do not delete prior entries.

---

## 2026-05-23 — Auto-Researcher v4

**Resume score at start of run:** 53 / 100

**Implemented on branch `claude/brave-bohr-dmZJS`:** none this run
(this seed entry only).

**Why this repo was deprioritized:** This is the lowest-scoring repo of
the six. The README is only ~315 bytes, there is no `tests/` directory,
no backend logic visible at the repo root beyond a single `app/` dir
and `index.html`, and the tech-stack prestige is modest (web + light
Python). The single highest-leverage move here is a README rewrite, but
that depends on understanding the actual feature surface — best done
in a focused follow-up run rather than a thin sweep.

**Evaluated and skipped this run:**
- *README rewrite (architecture, screenshots, setup steps).* The
  current README is essentially a placeholder. This is the right next
  move, but it needs the app actually running to capture screenshots
  and confirm setup commands.
- *Adding a first `tests/` directory + CI.* Tractable, but useless
  without at least one real assertion, which requires reading the
  backend code.
- *Switching the LLM provider to Anthropic Claude.* Likely the right
  long-term call (the project description mentions 'AI interview
  preparation') but needs scoped feature work.

**Next-run candidates (in priority order):**
1. Rewrite README: what it does, screenshot of the UI, exact setup
   commands, environment variables.
2. Add `tests/` with a smoke test for the FastAPI / Flask backend
   (whichever is actually wired up) and a CI workflow to run it.
3. Standardize the LLM client on Anthropic Claude with prompt caching.
4. Add a `.env.example` if missing.
