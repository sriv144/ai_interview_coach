# AI Interview Coach

AI-powered mock-interview platform that turns any job description into a
role-specific, voice-driven interview with structured per-question feedback
and a final coaching summary. Backend is FastAPI + WebSockets, LLM
orchestration is LangChain over Google Gemini, speech is Whisper (STT) +
gTTS (TTS), and the UI is a single static `index.html` that streams audio
over the WebSocket.

## What it does

1. The user uploads a job description PDF.
2. The backend parses the PDF and asks Gemini to generate five tailored
   interview questions.
3. For each question, the server synthesizes audio with gTTS, streams the
   question + audio over the WebSocket, and waits for the candidate's
   recorded answer.
4. The answer is transcribed locally with Whisper (`base` model) and
   evaluated by Gemini against the JD on three axes (relevance, clarity,
   impact) with a weighted total score and constructive feedback.
5. After the final question, a coaching summary aggregates the whole
   session into strengths, improvement areas, and an overall score.

## Architecture

```
  Browser (index.html)
        |  WebSocket  (binary audio in/out, JSON events)
        v
  FastAPI  app/main.py  --  /ws/interview
        |
        |--- app/utils/document_parser.py   (pypdf, JD -> text)
        |--- app/agents/question_generator.py  (Gemini -> 5 questions)
        |--- gTTS                              (question text -> mp3 bytes)
        |--- app/agents/answer_evaluator.py    (Whisper STT + Gemini eval)
        |--- app/agents/summary_generator.py   (Gemini final summary)
```

## Project layout

```
app/
  main.py                 FastAPI app + /ws/interview WebSocket handler
  schemas.py              Pydantic models for questions, evaluations, summary
  agents/
    question_generator.py JD -> 5 interview questions (Gemini)
    answer_evaluator.py   audio bytes -> Whisper transcript -> Gemini score
    summary_generator.py  full session -> final coaching summary
  utils/
    document_parser.py    pypdf PDF -> text
index.html                Single-file web UI (recorder + score cards)
requirements.txt          Pinned Python dependencies
.env.example              Environment template
```

## Requirements

- Python 3.10+ (Whisper needs a recent PyTorch wheel; 3.11 recommended).
- `ffmpeg` on PATH (Whisper uses it to decode the uploaded `.webm` audio).
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get install -y ffmpeg`
  - Windows: install from https://www.gyan.dev/ffmpeg/builds/ and add to PATH
- A Google AI Studio API key for Gemini.

## Quick start

```bash
# 1. Clone
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach

# 2. Create and activate a virtualenv
python -m venv .venv
source .venv/bin/activate            # macOS/Linux
# .\.venv\Scripts\activate           # Windows PowerShell

# 3. Install Python deps
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure secrets
cp .env.example .env
# edit .env and set GOOGLE_API_KEY

# 5. Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000 in a Chromium-based browser (the UI uses
`MediaRecorder` with the `webm` codec), upload a JD PDF, and start the
interview.

## How scoring works

`answer_evaluator.py` asks Gemini to score each answer on a 1-10 scale for
relevance, clarity, and impact, then computes a weighted total:

```
total = (relevance * 0.5) + (clarity * 0.25) + (impact * 0.25)
```

Relevance is weighted highest because answers that ignore the JD score low
even if they're well-delivered. The final summary averages the totals
across the five questions.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `GOOGLE_API_KEY` | Yes | Google AI Studio key for Gemini calls. |
| `GEMINI_MODEL` | No | Override the model name (default `gemini-1.5-flash-latest`). |

Whisper downloads `base` (~140MB) on first run and caches it under
`~/.cache/whisper`. Swap to `tiny` for faster CPU transcription or
`small`/`medium` for better accuracy in the call inside
`app/agents/answer_evaluator.py`.

## Troubleshooting

- **`ImportError: langchain_google_genai`** -- run `pip install -r
  requirements.txt` again; the project used to ship the wrong LangChain
  provider and a stale install will still have it.
- **`ValueError: GOOGLE_API_KEY not found in .env file`** -- the agents
  load `.env` via `python-dotenv`; make sure `.env` exists in the working
  directory you launched uvicorn from.
- **`FileNotFoundError: ffmpeg`** -- install ffmpeg as described above;
  Whisper shells out to it for `.webm` decoding.
- **WebSocket closes immediately after JD upload** -- the PDF couldn't be
  parsed. Try a different PDF or check the server logs for the pypdf
  error.

## Development

```bash
# Sanity-check that all modules import (catches the kind of drift this PR
# fixed):
python -m compileall app

# Quick smoke test for the document parser:
python -c "from app.utils.document_parser import parse_pdf_to_text; print('ok')"
```

A minimal GitHub Actions workflow at `.github/workflows/ci.yml` runs
`compileall` on every push so requirements drift can't sneak in unnoticed
again.

## License

MIT -- see [LICENSE](LICENSE).
