# AI Interview Coach

AI-powered mock-interview practice. Upload a job description and the app runs a
full spoken interview: it generates role-specific questions, reads them aloud,
listens to your spoken answers, and returns scored, constructive feedback in
real time — ending with an overall performance summary.

## Features

- **Job-description aware questions** — parses an uploaded JD (PDF) and uses
  Google Gemini to generate tailored interview questions.
- **Spoken questions** — each question is synthesized to audio with gTTS and
  streamed to the browser.
- **Voice answers, transcribed** — your recorded answer is transcribed locally
  with OpenAI Whisper, so no audio leaves your machine for speech-to-text.
- **Structured scoring** — every answer is graded on **relevance**, **clarity**,
  and **impact** (1–10) with a weighted total and written feedback.
- **Final summary** — after the last question, an overall report aggregates
  strengths, areas to improve, and an averaged score.
- **Real-time UX** — the whole session runs over a single WebSocket connection
  with a lightweight browser UI.

## How it works

```
Browser (index.html)
  │  1. upload JD (PDF bytes)
  ▼
FastAPI WebSocket  /ws/interview
  ├─ parse_pdf_to_text (pypdf)
  ├─ question_generator  ──▶ Gemini  (generate N questions from the JD)
  │     loop per question:
  ├─ gTTS  ──▶ question audio  ──▶ browser
  ├─ (browser records spoken answer) ──▶ audio bytes
  ├─ answer_evaluator    ──▶ Whisper (transcribe) + Gemini (score & feedback)
  └─ summary_generator   ──▶ Gemini  (final aggregated summary)
```

## Tech stack

| Layer            | Technology                                             |
| ---------------- | ------------------------------------------------------ |
| API / transport  | FastAPI, WebSockets, Uvicorn                            |
| LLM              | Google Gemini (`gemini-1.5-flash`) via LangChain       |
| Speech-to-text   | OpenAI Whisper (`base` model, runs locally)            |
| Text-to-speech   | gTTS                                                   |
| PDF parsing      | pypdf                                                  |
| Validation       | Pydantic schemas for every message and LLM output      |
| Frontend         | Single-page `index.html`                               |

## Prerequisites

- **Python 3.10+**
- **ffmpeg** on your `PATH` — required by Whisper for audio decoding
  (`apt install ffmpeg`, `brew install ffmpeg`, or `choco install ffmpeg`).
- A **Google Gemini API key** (free tier works): https://aistudio.google.com/app/apikey

The first run downloads the Whisper `base` model (~140 MB) automatically.

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key
cp .env.example .env            # Windows: copy .env.example .env
# edit .env and set GOOGLE_API_KEY
```

## Running

Start the server from the repository root so the `app` package and `index.html`
resolve correctly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000 in your browser, upload a job-description PDF,
and begin the interview.

## Project structure

```
.
├─ app/
│  ├─ main.py                     # FastAPI app + /ws/interview WebSocket loop
│  ├─ schemas.py                  # Pydantic models for messages & LLM outputs
│  ├─ agents/
│  │  ├─ question_generator.py    # JD -> interview questions (Gemini)
│  │  ├─ answer_evaluator.py      # audio -> transcript (Whisper) -> score (Gemini)
│  │  └─ summary_generator.py     # full history -> final summary (Gemini)
│  └─ utils/
│     └─ document_parser.py       # PDF -> text (pypdf)
├─ index.html                     # browser UI
├─ requirements.txt
└─ .env.example
```

## Roadmap

- Automated tests with mocked Gemini / Whisper, plus CI.
- Screenshots / a short demo recording in the README.
- A Dockerfile for one-command setup (bundling ffmpeg).
- Pinned dependency versions for reproducible installs.
