# Research Log

Persistent memory used by the auto-researcher agent. Each run appends a dated
section so future runs can see what was evaluated, what shipped, and what was
deliberately skipped.

## 2026-04-23 - Auto-Researcher v4

**Resume-worthiness score at start of run: 60 / 100**
- Tech stack prestige: 14/25 (Python backend + web UI for interview prep - solid but commodity)
- Commit recency: 22/25 (last push 2026-04-14, within window)
- Feature completeness: 11/20 (working but not flagship-grade)
- Stars / visibility: 5/15 (1 star, 1 open issue)
- README quality: 8/15 (functional but not polished)

### Branch
`claude/brave-bohr-ONkrp`

### Status this run
**Not selected for implementation.** Repo ranked 5th of 6 and the token
budget was spent on the top 3 (AegisQuant, embodied-skill-composer,
Autonomous-SRE-Agent). The two open claude/* branches already on this
repo (`beautiful-einstein-KSTnM`, `beautiful-einstein-TXG01`) hold prior
auto-researcher work that has not yet merged to main, so the highest
leverage next step is to review and merge those rather than stack a
fourth unreviewed branch.

### Prior claude/* branches observed (unmerged on main)
- `claude/beautiful-einstein-KSTnM`
- `claude/beautiful-einstein-TXG01`
- `auto-research/2026-04-14`

Contents not re-inspected this run to stay in token budget.

### Why this repo scored lower than the top 3
The interview-coach concept is useful but crowded - there are dozens of
similar projects on GitHub. To stand out it needs either a concrete
differentiator (e.g. audio analysis of delivery, structured STAR-answer
rubrics, comparable-benchmark dataset) or visible polish (demo gif,
live deploy, testimonials). Right now it reads as a generic LLM-backed
chat loop.

### Next-run candidates
1. Merge or close the two open `beautiful-einstein-*` branches so the
   auto-researcher has a clean main to work from.
2. Add a short "Why this is different" section to the README calling
   out the single highest-leverage differentiator.
3. Record a 60s demo gif / MP4 at `docs/demo.gif` and embed at the
   top of README.
4. Add one killer feature: structured STAR-method scoring returned as
   JSON (`{"situation": 0-10, "task": 0-10, ...}`) so answers can be
   graded across sessions.
5. Deploy a live demo (Streamlit Cloud / Vercel) and link from README.
