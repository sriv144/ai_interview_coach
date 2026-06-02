# AI Interview Coach

Real-time, voice-based interview practice over a single WebSocket. Upload a target job-description PDF, get tailored interview questions read aloud, answer with your microphone, and receive structured scoring + actionable feedback per answer plus a comprehensive final summary across the full session.

## Highlights

- Single-WebSocket interview loop, no page reloads.
- Job-description-driven question generation tailored to the target role.
- Whisper transcription of spoken answers.
- Structured scoring on a 1–10 scale: relevance, clarity, and impact, plus a weighted total.
- Constructive per-answer feedback and a comprehensive final summary across the full session.
- gTTS audio playback so questions are spoken back to the candidate.
- Pure FastAPI backend with a single static HTML frontend — runs locally in one Python process.

## Architecture

```
Browser (index.html)  ───── WebSocket ─────▶  FastAPI ( /ws/interview )
       │                                          │
       │   1. send JD pdf  ───────────────────▶ document_parser (pypdf)
       │                                          │
       │   2. {question text + audio}          ◀── question_generator (LLM → JSON schema)
       │                                          │   + gTTS synth
       │   3. send audio answer  ─────────────▶ answer_evaluator
       │                                          │   (Whisper transcribe → LLM scoring)
       │   4. {evaluation per question}        ◀──
       │
       │   ... loop over generated questions ...
       │
       │   5. {final_summary}                  ◀── summary_generator
```

### Modules

| Module | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI app, root HTML, `/ws/interview` WebSocket loop |
| `app/schemas.py` | Pydantic schemas: `InterviewQuestion`, `ScoreBreakdown`, `EvaluationResponse`, `InterviewTurn`, `FinalSummaryResponse` |
| `app/agents/question_generator.py` | Generates structured interview questions from JD text |
| `app/agents/answer_evaluator.py` | Whisper-transcribes audio and scores it against the JD and the asked question |
| `app/agents/summary_generator.py` | Produces final cross-turn summary and aggregate score |
| `app/utils/document_parser.py` | PDF → text via pypdf |
| `index.html` | Single-page frontend that drives the WebSocket and renders feedback |

## Stack

- Backend: FastAPI, Uvicorn, Pydantic v2
- LLM orchestration: LangChain (default provider is OpenAI via `langchain-openai`)
- Speech-to-text: OpenAI Whisper (local model)
- Text-to-speech: gTTS (Google Translate TTS endpoint, requires network)
- PDF parsing: pypdf
- Vector store reserved for future RAG: faiss-cpu

## Requirements

- Python 3.10+
- A working microphone in the browser (Chrome / Edge recommended)
- An LLM API key for the configured provider (OpenAI by default)

## Quick Start

Clone and create a virtual environment:

```bash
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

Configure environment:

```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=...
```

Run the app from the repository root so the WebSocket handler can serve `index.html`:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000> in your browser, upload a JD PDF, grant microphone access, and start the interview.

## WebSocket Protocol

The client opens a single connection to `ws://localhost:8000/ws/interview` and exchanges binary and JSON frames:

1. Client → Server (binary): JD PDF bytes.
2. Server → Client (json): `{"type": "question", "data": {"text": "...", "audio": "<base64 mp3>"}}`.
3. Client → Server (binary): the user's recorded answer audio.
4. Server → Client (json): `{"type": "evaluation", "data": EvaluationResponse}`.
5. Repeat 2–4 for every generated question.
6. Server → Client (json): `{"type": "final_summary", "data": FinalSummaryResponse}`.
7. Server → Client (json) on error: `{"error": "..."}`.

### Response schemas

`EvaluationResponse`:

```json
{
  "transcribed_text": "string",
  "feedback": "string",
  "total_score": 7.4,
  "score_breakdown": { "relevance": 8, "clarity": 7, "impact": 7 }
}
```

`FinalSummaryResponse`:

```json
{
  "overall_feedback": "string",
  "final_score": 7.6,
  "full_history": [ { "question": "...", "evaluation": { "...": "..." } } ]
}
```

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes (default provider) | — | LLM API key for question generation, scoring, and summary. |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Override the chat model used by `langchain-openai`. |
| `WHISPER_MODEL` | No | `base` | Whisper model size for transcription. |
| `HOST` | No | `127.0.0.1` | Uvicorn bind host. |
| `PORT` | No | `8000` | Uvicorn bind port. |

## Project Structure

```text
ai_interview_coach/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── agents/
│   │   ├── question_generator.py
│   │   ├── answer_evaluator.py
│   │   └── summary_generator.py
│   └── utils/
│       └── document_parser.py
├── index.html
├── requirements.txt
├── .env.example
└── README.md
```

## Troubleshooting

- "Could not parse the PDF." — Ensure the uploaded file is a text-bearing PDF, not a scanned image. OCR is not currently supported.
- WebSocket disconnects mid-session — Some browsers throttle the microphone when the tab is backgrounded. Keep the tab focused.
- `gTTS` fails offline — gTTS calls Google Translate's TTS endpoint and needs network access.
- Whisper is slow on first load — The model is downloaded and cached on first transcription.

## Roadmap

- Persisted session history with per-user accounts.
- RAG over a corpus of past interviews using the reserved `faiss-cpu` dependency.
- Side-by-side answer diffing across attempts.
- Configurable interview personas (behavioral, system-design, coding-prep).
- Dockerfile + one-shot Docker Compose stack.
