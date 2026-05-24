# AI Interview Coach

A real-time AI interview coach. Upload a job description (PDF), and the app generates role-specific questions, asks them aloud, listens to your spoken answer, scores it across relevance / clarity / impact, and produces a final summary at the end.

The backend is a single FastAPI service that drives the entire loop over a WebSocket. The frontend is a static HTML page served from the same process — no separate build step.

## How It Works

```text
        Browser (index.html, mic + audio playback)
                       │  WebSocket /ws/interview
                       ▼
           ┌───────────────────────────┐
           │     FastAPI WebSocket     │
           └─────────────┬─────────────┘
                         │ 1. JD PDF bytes
                         ▼
              pypdf → plain JD text
                         │
                         ▼
        question_generator  (LangChain + OpenAI)
          → list[InterviewQuestion]
                         │
           ┌─────────────┴─────────────┐
           │   for each question:      │
           │     gTTS  → question audio │ ──▶ browser plays it
           │     receive user audio    │ ◀── browser records answer
           │     answer_evaluator      │
           │       Whisper  → transcript│
           │       LLM      → score+feedback│
           │     send evaluation       │ ──▶ browser renders card
           └─────────────┬─────────────┘
                         │
                         ▼
           summary_generator (LangChain + OpenAI)
             → overall_feedback + final_score + full_history
```

Every message between client and server is a JSON `{ type, data }` envelope (see [WebSocket Protocol](#websocket-protocol)).

## Features

- Role-aware question generation driven by the uploaded JD, not a fixed bank.
- Spoken delivery of every question via gTTS so the practice loop feels closer to a live interview.
- Whisper-based transcription of the candidate's spoken answer, so practice is voice-first.
- Per-answer scoring with a structured breakdown: relevance, clarity, impact, plus free-form coaching feedback.
- Final summary at the end of the session: overall feedback, averaged score, and a replay of every question and evaluation.
- Pure WebSocket streaming — questions, audio, evaluations, and the final summary all flow over a single long-lived connection.
- Single-process deployment: FastAPI serves both the API and the static HTML frontend.

## Quick Start

Requirements: Python 3.10+ and `ffmpeg` on `PATH` (Whisper depends on it for audio decoding).

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# edit .env and set OPENAI_API_KEY

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Then open `http://127.0.0.1:8000/` in a modern browser, allow microphone access, upload a job description PDF, and start the interview.

## WebSocket Protocol

Endpoint: `GET ws://<host>/ws/interview`

The server treats binary frames as raw audio / PDF data and JSON frames as control messages. A full session looks like this:

| Step | Direction          | Frame   | Meaning                                                       |
|-----:|--------------------|---------|---------------------------------------------------------------|
| 1    | client → server    | binary  | Job description PDF bytes                                     |
| 2    | server → client    | json    | `{type: "question", data: {text, audio (base64 mp3)}}`        |
| 3    | client → server    | binary  | User's spoken answer (audio bytes)                            |
| 4    | server → client    | json    | `{type: "evaluation", data: EvaluationResponse}`              |
| 5    | (loop steps 2-4 for each generated question)                                            |
| 6    | server → client    | json    | `{type: "final_summary", data: FinalSummaryResponse}`         |
| —    | server → client    | json    | `{error: "..."}` on any unrecoverable error                   |

Response schemas (full Pydantic models in `app/schemas.py`):

```text
EvaluationResponse {
  transcribed_text: str
  feedback:         str
  total_score:      float (1..10)
  score_breakdown:  { relevance: 1..10, clarity: 1..10, impact: 1..10 }
}

FinalSummaryResponse {
  overall_feedback: str
  final_score:      float (1..10)
  full_history:     [ { question: str, evaluation: EvaluationResponse } ]
}
```

## Configuration

| Variable          | Required | Default                  | Purpose                                                                 |
|-------------------|----------|--------------------------|-------------------------------------------------------------------------|
| `OPENAI_API_KEY`  | yes      | —                        | Used by `langchain-openai` for question generation, answer evaluation, and final summary |
| `OPENAI_MODEL`    | no       | (LangChain default)      | Override the chat model used by the agents                              |
| `WHISPER_MODEL`   | no       | `base`                   | Whisper model size for transcription (`tiny`, `base`, `small`, ...)     |
| `TTS_LANG`        | no       | `en`                     | gTTS language code for spoken questions                                 |

A template is provided in `.env.example`. The application loads it automatically via `python-dotenv`.

## Project Structure

```text
.
├── app/
│   ├── main.py                  # FastAPI app + /ws/interview WebSocket loop
│   ├── schemas.py               # Pydantic models for questions, evaluations, summary, ws envelopes
│   ├── agents/
│   │   ├── question_generator.py  # LangChain agent: JD → interview questions
│   │   ├── answer_evaluator.py    # Whisper transcription + LangChain agent: answer → score + feedback
│   │   └── summary_generator.py   # LangChain agent: full history → overall feedback + final score
│   └── utils/
│       └── document_parser.py     # PDF → text via pypdf
├── index.html                   # Static frontend served from `/`
├── requirements.txt
├── .env.example
└── .github/workflows/ci.yml     # Lint + syntax check on push / PR
```

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **LLM Orchestration:** LangChain, langchain-openai
- **Audio:** gTTS (text-to-speech for questions), openai-whisper (speech-to-text for answers)
- **Documents:** pypdf (JD parsing)
- **Vector store (planned):** FAISS — currently a dependency only, reserved for upcoming JD/resume retrieval features.

## Notes & Troubleshooting

- **`ffmpeg` not found / Whisper fails to decode**: install ffmpeg system-wide (`brew install ffmpeg`, `choco install ffmpeg`, or `apt install ffmpeg`).
- **No audio plays in the browser**: most browsers require a user gesture (a click) before playing audio. The included `index.html` handles this on the start button.
- **`No API key` from LangChain**: confirm `OPENAI_API_KEY` is in `.env` and that `python-dotenv` is loading it (FastAPI imports `app.main`, which expects the variable to already be in the environment when `langchain-openai` initialises).
- **PDF can't be parsed**: scanned / image-only PDFs are not OCR'd. Use a text-based JD export.

## Roadmap

- Persist sessions and let users replay past interviews.
- Resume-aware questioning (use the existing FAISS dependency to retrieve relevant resume snippets).
- Configurable difficulty (junior / mid / senior) and question style (behavioral / system design / coding).
- Optional video capture for tone / pace feedback.
- Pluggable LLM providers (Anthropic / local models) behind the existing agent interfaces.
