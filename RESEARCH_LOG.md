# Research Log

This file tracks autonomous research and improvement runs against this
repository.

## 2026-04-27 — Auto-Researcher v4

**Resume score at start of run:** 43 / 100 — ranked 6 of 6 in the portfolio.

**Branch:** `claude/brave-bohr-snPHW`.

### Implemented this run

No code changes. This commit only seeds the research log so future runs have
memory of what was already evaluated.

### Why no implementation this run

The README is currently a 6-line snippet, which makes it impossible to know
without reading source code which features actually exist (real-time AI
feedback? speech-to-text? video? live coding panels?). Implementing CI or
polishing the README *blind* risks documenting features that don't exist or
adding tests that don't match the actual surface. Token budget for this run
was prioritized for repos where the surface was already legible.

### Evaluated and parked for next run

- **README expansion** is the biggest single lever, but it requires reading
  `app/main.py` and surrounding modules to inventory what is actually
  implemented before writing it. Treat it as the first task next run.
- **`.env.example`:** README references `cp .env.example .env` but its
  presence is unverified. Confirm or add.
- **CI:** add pytest workflow once the test surface is known.
- **LICENSE:** missing.
- **Screenshot or recorded demo:** an interview-prep tool benefits hugely
  from a UI screenshot.

### Next-run candidates (priority order)

1. Inventory `app/` source code, then rewrite README with feature list,
   architecture, and a screenshot.
2. Verify or create `.env.example`.
3. Add CI (pytest).
4. Add LICENSE.
