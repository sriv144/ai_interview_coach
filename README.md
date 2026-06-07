# AI Interview Coach

Real-time, voice-driven mock interviews powered by a multi-agent LLM pipeline. Upload a Job Description PDF, and the system role-plays a tailored technical/behavioral interview over a live WebSocket — generating questions, listening to your spoken answers, evaluating them, and producing a structured final report.

## Why this exists

Generic interview prep tools ask canned questions and grade against canned rubrics. This project ingests the *actual* JD you're targeting and grounds every question and every evaluation in that specific role's requirements. Three specialized agents work together so each stage is optimized in isolation rather than crammed into one mega-prompt.

## Architecture

```
                Browser (mic + audio playback)
                          │  WebSocket /ws/interview
                          ▼
               ┌────────────────────────┐
               │   FastAPI WebSocket    │
               └──────────┬─────────────┘
                          │
                          ▼
            ┌──────────────────────────────┐
            │      Multi-Agent Pipeline    │
            │                              │
            │   1. question_generator      │  ← JD text → tailored Q list
            │   2. answer_evaluator        │  ← audio + Q + JD → feedback
            │   3. summary_generator       │  ← full transcript → report
            └──────────────┬───────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
        PyPDF2 (JD parse)        gTTS (Q → audio)
                                 Whisper (audio → text)
```

Each turn flows through the WebSocket:

1. Client uploads JD PDF as bytes → server parses with `PyPDF2`.
2. `question_generator` produces a structured question list grounded in the JD.
3. For each question:
   - Server synthesizes audio via `gTTS`, base64-encodes, ships it to the browser.
   - Browser plays the question and records the spoken answer.
   - Server transcribes with `openai-whisper` (runs locally, no API call), then `answer_evaluator` scores the response against both the question and JD.
   - Per-question feedback is sent back live.
4. After the final question, `summary_generator` produces an end-of-session report covering strengths, weaknesses, and concrete improvement areas.

## Features

- **JD-grounded questions** — every question is generated from your uploaded job description, not a static bank.
- **Voice in, voice out** — `gTTS` for question playback, local `openai-whisper` for answer transcription (no third-party STT API).
- **Streaming WebSocket UX** — questions, evaluations, and the final summary all stream back as structured Pydantic-validated JSON messages.
- **Multi-agent design** — question generation, answer evaluation, and final summary are independent LLM agents (`app/agents/`), each with its own focused prompt.
- **Structured outputs end-to-end** — `app/schemas.py` defines `WebSocketMessage`, `InterviewTurn`, evaluation payloads, etc. for safe client handling.
- **PDF intake** — drop in any JD; `PyPDF2` extracts the text.

## Tech stack

| Layer | Choice |
|-------|--------|
| Backend | FastAPI + Uvicorn |
| Realtime | WebSockets |
| LLM | Google Gemini (`gemini-1.5-flash-latest`) via `langchain-google-genai` |
| LLM orchestration | LangChain |
| TTS | gTTS |
| STT | openai-whisper (local) |
| PDF | PyPDF2 |
| Validation | Pydantic v2 |
| Frontend | Single-page `index.html` with mic capture + audio playback |

## Project structure

```
.
├── app/
│   ├── main.py                # FastAPI app + /ws/interview WebSocket handler
│   ├── schemas.py             # Pydantic models for socket messages, turns, evaluations
│   ├── agents/
│   │   ├── question_generator.py   # JD → structured question list (Gemini)
│   │   ├── answer_evaluator.py     # (audio, Q, JD) → per-answer evaluation (Whisper + Gemini)
│   │   └── summary_generator.py    # transcript → final report (Gemini)
│   └── utils/
│       └── document_parser.py # PyPDF2 wrapper
├── index.html                 # Browser UI (upload JD, talk, see feedback)
├── requirements.txt
├── .env.example
└── .github/workflows/ci.yml
```

## Quick start

```bash
# 1. Create venv
python -m venv venv
# Windows: venv\Scripts\activate
# macOS / Linux: source venv/bin/activate

# 2. Install deps
pip install -r requirements.txt

# 3. Configure env
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY (https://aistudio.google.com/app/apikey)

# 4. Run the server
uvicorn app.main:app --reload --port 8000
```

Then open <http://localhost:8000> in your browser, allow microphone access, upload a JD PDF, and start the mock interview.

> First run with `openai-whisper` will download a model file (~150 MB for the default tier). To use a smaller / larger model, edit the size argument inside `app/agents/answer_evaluator.py`.

## Environment variables

See `.env.example` for the full list. At minimum you need `GOOGLE_API_KEY` for the Gemini-backed agent layer. Whisper runs locally and does not need an API key.

## Roadmap

- [ ] Persist interview sessions to disk for resume / replay
- [ ] FAISS-backed retrieval over a personal experience corpus (resume + STAR stories) so evaluations can flag missed selling points
- [ ] Resume PDF intake on the same WebSocket and cross-reference against JD gaps
- [ ] Side-by-side ideal-answer rubric in the per-question feedback panel
- [ ] Dockerfile + one-command deploy
- [ ] Pluggable LLM provider (swap Gemini for Anthropic Claude / OpenAI behind one interface)
- [ ] Migrate PDF parsing from `PyPDF2` (legacy) to the maintained `pypdf` package

## Contributing

PRs welcome. Keep agent prompts in their own files under `app/agents/` and always return Pydantic-validated objects so the WebSocket contract stays stable.

## License

MIT — see [LICENSE](LICENSE).
