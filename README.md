# AI Interview Coach

A real-time mock-interview coach that turns a job description PDF into a
spoken, role-specific interview, scores each answer, and produces a final
coaching summary. Runs as a FastAPI WebSocket service with a single-page
browser UI.

## How it works

```
  Browser (index.html)
      |  WebSocket /ws/interview
      v
  FastAPI app (app/main.py)
      |
      +-- document_parser  -- PyPDF2 ----------- extract JD text
      |
      +-- question_generator -- Gemini --------- 5 role-specific questions
      |                                          (Pydantic-validated JSON)
      |
      +-- gTTS -------------------------------- speak each question
      |                                          (audio sent to browser)
      |
      +-- (browser records candidate answer, sends webm bytes back)
      |
      +-- answer_evaluator -- Whisper --------- transcribe answer
      |                    -- Gemini ---------- score relevance / clarity / impact
      |                                          + constructive feedback
      |
      +-- summary_generator -- Gemini --------- overall feedback + final score
```

All LLM calls are schema-bound via `PydanticOutputParser`, so the WebSocket
frames the browser receives are always well-typed.

## Features

- Job-description-driven question generation (Gemini 1.5 Flash).
- Voice-in, voice-out flow: questions are spoken with gTTS, answers are
  recorded in the browser and transcribed locally with Whisper.
- Per-answer scoring with a transparent rubric (relevance 50% / clarity 25%
  / impact 25%) and constructive written feedback.
- Final summary call that aggregates the whole session: strengths, areas to
  improve, and a final average score.
- WebSocket protocol with typed message frames (`question`,
  `evaluation`, `final_summary`, `error`).

## Project layout

```
app/
  main.py                  FastAPI app + WebSocket handler
  schemas.py               Pydantic models for all WS frames
  agents/
    question_generator.py  JD -> 5 questions
    answer_evaluator.py    audio + question -> transcript + scored feedback
    summary_generator.py   full history -> overall summary
  utils/
    document_parser.py     PDF -> text (PyPDF2)
index.html                 Single-page browser UI
requirements.txt           Python dependencies
.env.example               Environment template
```

## Requirements

- Python 3.11+ recommended.
- A Google Gemini API key with access to `gemini-1.5-flash-latest`.
- `ffmpeg` available on PATH (used by openai-whisper for audio decoding).

## Quick start

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # then edit .env and set GOOGLE_API_KEY
python -m uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` and upload a job-description PDF to begin the
mock interview.

## WebSocket protocol

The browser opens `ws://localhost:8000/ws/interview` and exchanges these
messages with the server:

| Direction | Payload | Meaning |
|-----------|---------|---------|
| client -> server | raw PDF bytes | the job description |
| server -> client | `{ type: "question", data: { text, audio } }` | next question, base64 mp3 |
| client -> server | raw webm bytes | candidate's spoken answer |
| server -> client | `{ type: "evaluation", data: EvaluationResponse }` | per-answer feedback |
| server -> client | `{ type: "final_summary", data: FinalSummaryResponse }` | end-of-interview summary |
| server -> client | `{ error: "..." }` | unrecoverable error |

The schemas are defined in `app/schemas.py` and validated end-to-end with
Pydantic.

## Notes on cost & privacy

- Whisper runs locally (the `base` model is loaded at startup), so audio
  never leaves the host.
- Text is sent to Gemini for question generation, evaluation, and summary.
- gTTS reaches Google Translate's TTS endpoint to synthesize question audio.

## Roadmap

- Persist sessions and let candidates review past interviews.
- Add an explicit STAR-format rubric for behavioral answers.
- Optional retrieval over the candidate's resume to ground answers.
- Swap Whisper-base for a streaming ASR backend for lower latency.
