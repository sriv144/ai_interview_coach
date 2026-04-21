# AI Interview Coach

A real-time AI interview simulator. Upload a job description, and the app generates role-specific questions, plays them back as speech, listens to your spoken answers, transcribes them with Whisper, and returns structured feedback plus a final performance summary.

## How It Works

```
  PDF JD upload ──▶ WebSocket /ws/interview
                         │
                         ▼
            ┌────────────────────────┐
            │  question_generator    │  LangChain + OpenAI
            │  → N tailored questions│
            └────────────┬───────────┘
                         ▼
            ┌────────────────────────┐
            │  gTTS text-to-speech   │  Sent as base64 audio
            └────────────┬───────────┘
                         ▼
            [ user records audio answer ]
                         ▼
            ┌────────────────────────┐
            │  answer_evaluator      │  Whisper STT + LLM judge
            │  → relevance / clarity │  (1–10 per axis)
            │    / impact + feedback │
            └────────────┬───────────┘
                         ▼
            ┌────────────────────────┐
            │  summary_generator     │  After all turns
            │  → overall score +     │
            │    strengths / gaps    │
            └────────────────────────┘
```

## Features

- **JD-grounded question generation** — questions reflect the actual role, not generic templates.
- **Spoken answer evaluation** — OpenAI Whisper transcribes audio, the LLM rubric-scores the answer.
- **Three-axis scoring rubric** — relevance, clarity, and impact (1–10 each), plus a weighted total.
- **Natural voice delivery** — gTTS synthesizes each question as audio for a realistic feel.
- **Full-session summary** — consolidated strengths, gaps, and an overall score across all turns.
- **Streaming UX** — everything rides a single WebSocket, with feedback for each answer as soon as it's ready.

## Tech Stack

| Layer | Choice |
|---|---|
| API | FastAPI + WebSockets |
| LLM orchestration | LangChain, `langchain-openai` |
| Speech-to-text | `openai-whisper` (local) |
| Text-to-speech | gTTS |
| PDF parsing | `pypdf` |
| Vector store (future RAG) | FAISS (`faiss-cpu`) |
| Frontend | Single-page `index.html` (vanilla JS, Web Audio API) |

## Quick Start

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env          # fill in your OpenAI key
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/` in a browser.

> Whisper downloads its model on first use, so the first answer evaluation may take longer than subsequent ones. For a lighter model, set `WHISPER_MODEL=tiny` (or `base`, `small`, `medium`) in `.env` before starting the server.

## Environment

Set these in `.env` (see `.env.example`):

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | OpenAI key for question generation, answer evaluation, and summary. |
| `OPENAI_MODEL` | No | Chat model override. Defaults to the model selected inside each agent. |
| `WHISPER_MODEL` | No | Whisper size (`tiny`, `base`, `small`, `medium`, `large`). Smaller = faster, less accurate. |

## WebSocket Protocol — `/ws/interview`

The client and server exchange a mix of binary frames (audio/PDF) and JSON frames (messages).

1. **Client → Server (bytes)**: the raw PDF bytes of the job description.
2. For each generated question, **server → client (JSON)**:
   ```json
   { "type": "question", "data": { "text": "...", "audio": "<base64 mp3>" } }
   ```
3. **Client → Server (bytes)**: the raw audio bytes of the spoken answer.
4. **Server → client (JSON)**: per-answer evaluation:
   ```json
   {
     "type": "evaluation",
     "data": {
       "transcribed_text": "...",
       "feedback": "...",
       "total_score": 7.8,
       "score_breakdown": { "relevance": 8, "clarity": 7, "impact": 8 }
     }
   }
   ```
5. When all questions are answered, **server → client (JSON)**:
   ```json
   {
     "type": "final_summary",
     "data": {
       "overall_feedback": "...",
       "final_score": 7.4,
       "full_history": [ { "question": "...", "evaluation": { ... } } ]
     }
   }
   ```

At any point, an error frame may be sent: `{ "type": "error", "error": "..." }`.

## Project Layout

```
app/
  main.py                 FastAPI app + WebSocket interview loop
  schemas.py              Pydantic schemas (questions, evaluation, summary, WS envelopes)
  agents/
    question_generator.py Generates role-specific questions from the JD
    answer_evaluator.py   Whisper STT + LLM rubric scoring
    summary_generator.py  End-of-interview aggregate feedback
  utils/
    document_parser.py    PDF → text extraction
index.html                Single-page frontend (mic capture + playback + UI)
requirements.txt
.env.example
```

## Roadmap

- Resume upload + cross-reference against JD for personalized questions
- JD-specific RAG over a curated interview-question corpus (FAISS is already wired in `requirements.txt`)
- Follow-up question generation based on candidate answers
- Session persistence and shareable interview reports
- Auth + per-user history
