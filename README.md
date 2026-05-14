# AI Interview Coach

A browser-based mock interview tool that turns a job description PDF into a
five-question voice interview, scores each answer in real time, and produces
a final performance summary.

The backend is FastAPI with a single WebSocket endpoint. The frontend is a
vanilla `index.html` page that records audio answers in the browser. Question
generation, scoring, and the final summary are powered by Google Gemini via
LangChain. Audio is transcribed locally with OpenAI Whisper.

## Features

- **Job-description-aware questions:** upload a JD PDF and Gemini generates
  five role-specific interview questions.
- **Voice-first loop:** each question is spoken back over WebSocket using
  gTTS, and the candidate records audio answers from the browser.
- **Local speech-to-text:** answers are transcribed with Whisper running
  locally (no audio leaves the box once the model is loaded).
- **Per-answer scoring:** every turn returns a Relevance / Clarity / Impact
  breakdown (1–10 each) and a weighted total
  `Total = 0.5·Relevance + 0.25·Clarity + 0.25·Impact`.
- **Constructive feedback per turn:** one positive observation and one to two
  concrete improvements per answer.
- **Final summary:** an aggregate overall-feedback + final score across all
  five turns, with the full transcript and breakdown returned to the UI.

## Tech Stack

- **Backend:** FastAPI, Uvicorn, Pydantic
- **LLM:** Google Gemini 1.5 Flash via `langchain-google-genai`
- **Speech-to-text:** OpenAI Whisper (`base` model, runs locally)
- **Text-to-speech:** gTTS
- **PDF parsing:** pypdf
- **Frontend:** single-page `index.html`, vanilla JS, MediaRecorder API

## Project Structure

```text
app/
  main.py                          FastAPI app + /ws/interview WebSocket loop
  schemas.py                       Pydantic request/response models
  agents/
    question_generator.py          Gemini chain that produces 5 questions
    answer_evaluator.py            Whisper transcription + Gemini scoring
    summary_generator.py           Final aggregate summary across all turns
  utils/
    document_parser.py             PDF → text helper
index.html                         Single-page browser UI
requirements.txt                   Python dependencies
.env.example                       Environment template (GOOGLE_API_KEY)
```

## WebSocket Protocol (`/ws/interview`)

| Direction | Payload                                | Purpose                                              |
| --------- | -------------------------------------- | ---------------------------------------------------- |
| C → S     | raw bytes (PDF)                        | Upload the job description                            |
| S → C     | `{type: "question", data: {text, audio}}` | Next question, with base64-encoded MP3 from gTTS    |
| C → S     | raw bytes (audio/webm)                 | Candidate's recorded answer                           |
| S → C     | `{type: "evaluation", data: {...}}`     | Per-turn transcript + scores + feedback              |
| S → C     | `{type: "final_summary", data: {...}}` | End-of-interview aggregate after the fifth turn      |
| S → C     | `{type: "error", error: "..."}`         | Server-side error                                    |

See `app/schemas.py` for full Pydantic models.

## Quick Start

```bash
# 1. Clone and enter
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach

# 2. Create a virtualenv
python -m venv venv
# Linux / macOS:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# 3. Install deps
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure secrets
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY=...

# 5. Run the app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` in the browser. The same page serves the UI and
upgrades to the WebSocket interview loop.

## Requirements

- Python 3.11 or newer.
- A Google Gemini API key (`GOOGLE_API_KEY`).
- `ffmpeg` available on `PATH` (required by Whisper to decode browser-recorded
  WebM audio).
- First run downloads the Whisper `base` model (~140 MB) into the local cache.

## Environment Variables

| Variable          | Required | Description                                     |
| ----------------- | -------- | ----------------------------------------------- |
| `GOOGLE_API_KEY`  | Yes      | Used by question generation, scoring, summary   |

## Notes

- Whisper runs locally; transcripts never leave your machine.
- Question generation, scoring, and final summary are all Gemini calls.
- The `faiss-cpu` dependency is reserved for upcoming retrieval-augmented
  features (resume + job-description grounding) and is not used by the current
  WebSocket flow.
- This repository is an interview-prep practice tool, not a hiring decision
  system. Scores are heuristic guidance only.

## License

MIT — see [`LICENSE`](./LICENSE).
