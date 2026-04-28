# AI Interview Coach

A real-time, voice-driven interview coach. Upload a job description (PDF) and the system generates tailored interview questions, listens to your spoken answers over a WebSocket, evaluates each answer with a structured rubric, and produces a final interview summary.

Built as an end-to-end LLM application that combines document parsing, multi-agent question generation, audio transcription, scored rubric evaluation, and TTS — all streamed over a single WebSocket session.

## Highlights

- **PDF job-description ingestion** with PyPDF parsing.
- **Question generator agent** that produces role-specific interview questions from the JD.
- **Voice answer evaluation** — Whisper transcribes the user audio, then an evaluator agent scores the response on relevance, clarity, and impact (1–10 each) and returns structured feedback.
- **Final summary agent** that aggregates all turns into an overall score and qualitative review.
- **Bi-directional voice loop** — questions are spoken back to the user via gTTS, answers are streamed in as audio bytes.
- **Strict Pydantic schemas** for every WebSocket payload (question, evaluation, final summary, error).
- **Single-page web client** (`index.html`) for end-to-end manual testing in the browser.

## Architecture

```
               ┌───────────────────┐                  ┌─────────────┐
               │ Browser (index.html) │ ◄─ WebSocket ─►│ FastAPI app │
               └───────────────────┘                  └────┬───────┘
                                                       │
            ┌───────────────────────────────────────────────┴───────┐
            │                                                          │
     ┌───────▼────────┐   ┌──────────────┐   ┌────────────────┐   ┌─────▼─────────┐
     │ Document Parser  │──►│ Question Gen │──►│ Answer Evaluator│──►│ Summary Agent  │
     │ (PDF → text)     │   │ LLM agent    │   │ Whisper + LLM  │   │ LLM aggregate  │
     └────────────────┘   └──────────────┘   └────────────────┘   └───────────────┘
```

### WebSocket protocol (`/ws/interview`)

1. Client opens connection.
2. Client sends raw PDF bytes (the job description).
3. Server parses the PDF, calls the question-generator agent, then loops:
   - Sends `{type: "question", data: {text, audio (base64 mp3)}}`.
   - Receives raw audio bytes (the candidate's spoken answer).
   - Sends `{type: "evaluation", data: EvaluationResponse}` with transcript, feedback, weighted score, and a per-axis score breakdown.
4. After the last question, the server sends `{type: "final_summary", data: FinalSummaryResponse}` with the overall score, narrative feedback, and full turn history.
5. Server sends `{type: "error", data: ...}` and closes on any failure.

All payloads are validated by Pydantic models in `app/schemas.py`.

## Tech Stack

- **Backend**: FastAPI, Uvicorn, WebSockets, Pydantic.
- **LLM orchestration**: LangChain (`langchain`, `langchain-openai`).
- **Speech-to-text**: OpenAI Whisper (local model).
- **Text-to-speech**: gTTS.
- **PDF parsing**: PyPDF.
- **Future retrieval**: FAISS (declared, used to support a JD knowledge base).
- **Frontend**: single static `index.html` page (no framework, vanilla JS for WebSocket + audio capture).

## Project Structure

```
.
├── app/
│   ├── main.py                  # FastAPI app, WebSocket endpoint, interview loop
│   ├── schemas.py               # Pydantic models for every WebSocket payload
│   ├── agents/
│   │   ├── question_generator.py  # JD → List[InterviewQuestion]
│   │   ├── answer_evaluator.py    # Audio + JD + Q → EvaluationResponse
│   │   └── summary_generator.py   # Turn history → FinalSummaryResponse
│   └── utils/
│       └── document_parser.py     # PDF bytes → plain text
├── index.html                   # Browser client (mic capture, audio playback, score UI)
├── requirements.txt
├── .env.example                 # Required environment variables
└── README.md
```

## Quick Start

```bash
# 1. Clone and create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in a modern browser, allow microphone access, and upload a JD PDF to begin.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Used by the LangChain agents (question generator, answer evaluator, summary generator). |
| `OPENAI_MODEL` | No | Override the default chat model. |
| `WHISPER_MODEL` | No | Whisper model size (e.g. `base`, `small`). Defaults to a small local model. |
| `LOG_LEVEL` | No | Logging verbosity. Defaults to `INFO`. |

A template lives in `.env.example`.

## Roadmap

- Persist interview history per user with a lightweight database.
- Add a FAISS-backed retrieval layer so the question generator can pull from a JD/role knowledge base.
- Streaming evaluation feedback (token-by-token) instead of one shot per question.
- Multi-language interviews (already trivially supported by gTTS for TTS).
- Dockerfile + GitHub Actions CI for tests and lint.

## Notes

- The current `requirements.txt` declares `openai-whisper`, which downloads a model the first time the evaluator runs. Allow extra time on the first answer.
- gTTS requires outbound network access to Google's TTS endpoint.
- The WebSocket endpoint expects exactly one PDF on connection followed by N answer audio blobs — see `app/main.py` for the precise sequence.
