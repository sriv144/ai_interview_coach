# AI Interview Coach

Real-time AI-powered interview practice. Upload a job description PDF, answer spoken questions, and get per-answer and overall feedback with a weighted score breakdown — all over a single WebSocket connection.

## Features

- **JD-aware question generation.** Upload any job description PDF; an LLM generates a tailored interview question set.
- **Voice-first loop.** Questions are spoken to you via TTS (gTTS); you respond with your microphone.
- **Whisper transcription + structured scoring.** Each answer is transcribed and scored 1–10 on **relevance**, **clarity**, and **impact**, with written feedback.
- **Final summary.** At the end of the session you get an overall score, qualitative summary, and the full question-by-question history.
- **Single WebSocket protocol.** All exchanges flow over `/ws/interview` — simple to host, easy to extend.

## Architecture

```
Browser (index.html)
    │  WebSocket /ws/interview
    ▼
FastAPI (app/main.py)
    ├─ document_parser → pypdf      (JD PDF → text)
    ├─ question_generator (LangChain + OpenAI)
    ├─ gTTS                          (question audio)
    ├─ answer_evaluator (Whisper + LangChain)
    └─ summary_generator             (final report)
```

## Tech Stack

- **Backend:** FastAPI, Uvicorn, WebSockets
- **LLM orchestration:** LangChain + langchain-openai
- **Speech:** OpenAI Whisper (STT), gTTS (TTS)
- **PDF parsing:** pypdf
- **Validation:** Pydantic v2
- **Frontend:** Static `index.html` (vanilla JS + Web Audio API)

## Quick Start

```bash
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # then edit .env and set OPENAI_API_KEY

python -m uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser, allow microphone access, and upload a JD PDF to start.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | **Yes** | Used for both question generation and answer evaluation |
| `OPENAI_MODEL` | No | Chat model override (default: `gpt-4o-mini`) |
| `WHISPER_MODEL` | No | Whisper model size (default: `base`) — use `small` or `medium` for higher accuracy |

## WebSocket Protocol

Endpoint: `GET /ws/interview` (WebSocket upgrade)

| Direction | Payload | Meaning |
| --- | --- | --- |
| client → server | binary (PDF) | Job description to tailor questions from |
| server → client | `{type: "question", data: {text, audio}}` | Next question (audio = base64 MP3) |
| client → server | binary (audio/webm) | User's spoken answer |
| server → client | `{type: "evaluation", data: EvaluationResponse}` | Per-answer score + feedback |
| server → client | `{type: "final_summary", data: FinalSummaryResponse}` | End-of-interview report |
| server → client | `{type: "error", error: "..."}` | Any failure |

See `app/schemas.py` for the full Pydantic contracts.

## Project Structure

```
.
├── app/
│   ├── main.py                   # FastAPI + WebSocket entrypoint
│   ├── schemas.py                # Pydantic models
│   ├── agents/
│   │   ├── question_generator.py # JD → questions
│   │   ├── answer_evaluator.py   # audio → transcript + score
│   │   └── summary_generator.py  # history → final report
│   └── utils/
│       └── document_parser.py    # PDF → text
├── index.html                    # Frontend (served at /)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Roadmap

- Persist sessions to disk (SQLite) so users can resume
- Support `.docx` and pasted-text JDs in addition to PDF
- Swap Whisper for faster-whisper / local GPU inference
- Add a role-specific question bank (behavioral vs. systems vs. ML)
- Optional RAG over the user's resume for more personal follow-ups

## License

MIT — see `LICENSE` if present, otherwise treat as MIT.
