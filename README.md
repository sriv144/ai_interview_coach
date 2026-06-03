# AI Interview Coach

[![CI](https://github.com/sriv144/ai_interview_coach/actions/workflows/ci.yml/badge.svg)](https://github.com/sriv144/ai_interview_coach/actions/workflows/ci.yml)

An end-to-end interview practice loop: drop in a job description PDF,
the app generates role-specific questions, asks them out loud (TTS),
listens to your spoken answer (Whisper STT), scores each answer on
relevance / clarity / impact, and at the end produces a full session
debrief with an overall score.

Front-end and back-end talk over a single WebSocket so the entire
interview — questions, audio, evaluations, and final summary —
streams in real time.

## How it works

```
   index.html (browser)
        |
        | upload JD .pdf (bytes)
        | mic-recorded answers (bytes)
        v
   FastAPI  /ws/interview  (WebSocket)
        |
        +-- parse PDF             (pypdf)
        +-- question_generator    (LLM)  -> 5 role-specific questions
        +-- TTS each question     (gTTS) -> mp3 stream to browser
        +-- answer_evaluator      (Whisper + LLM)
        |       -> transcribed_text
        |       -> score_breakdown { relevance, clarity, impact }
        |       -> total_score, written feedback
        +-- summary_generator     (LLM)  -> overall_feedback + final_score
```

All messages are typed Pydantic models (see `app/schemas.py`).

## Stack

| Layer | Choice |
|---|---|
| Web framework | FastAPI + Uvicorn |
| Realtime transport | Native WebSocket (`/ws/interview`) |
| Front-end | Single-page `index.html` (vanilla JS + MediaRecorder API) |
| LLM orchestration | LangChain + Pydantic output parsers |
| LLM provider | Google Gemini (`gemini-1.5-flash-latest`) via `langchain-google-genai` |
| Speech in | OpenAI Whisper (`openai-whisper`, local) |
| Speech out | gTTS |
| PDF parsing | pypdf |

A `langchain-openai` dependency is also pinned so the agents can be
swapped to an OpenAI-compatible provider with no code change to the
LangChain `chain | model | parser` wiring.

## Project layout

```
.
├── app/
│   ├── main.py                # FastAPI app + /ws/interview state machine
│   ├── schemas.py             # Pydantic types shared with the browser
│   ├── agents/
│   │   ├── question_generator.py   # JD -> 5 InterviewQuestion objects
│   │   ├── answer_evaluator.py     # audio + JD + question -> EvaluationResponse
│   │   └── summary_generator.py    # full history -> FinalSummaryResponse
│   └── utils/
│       └── document_parser.py      # pypdf wrapper
├── index.html                 # single-page client (mic + audio playback)
├── requirements.txt
├── .env.example
└── .github/workflows/ci.yml
```

## Quick start

```bash
# 1. Create + activate a venv
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 2. Install deps
pip install --upgrade pip
pip install -r requirements.txt
# Whisper needs ffmpeg in PATH
#   macOS:   brew install ffmpeg
#   Ubuntu:  sudo apt-get install -y ffmpeg
#   Windows: choco install ffmpeg   (or download from ffmpeg.org)

# 3. Configure secrets
cp .env.example .env
# edit .env and set GOOGLE_API_KEY=...

# 4. Run
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>, upload a job description PDF, and
talk through the questions.

## Environment variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | yes | Gemini key used by the three LangChain agents. |
| `OPENAI_API_KEY` | no | Optional — only needed if you swap the chains to `langchain-openai`. |

## WebSocket protocol

Every message is `WebSocketMessage { type, data }`.

| `type` | direction | `data` shape |
|---|---|---|
| (raw bytes) | client → server | initial JD PDF, then each recorded answer |
| `question` | server → client | `{ text, audio }` where `audio` is base64-encoded mp3 |
| `evaluation` | server → client | `EvaluationResponse` for the last answer |
| `final_summary` | server → client | `FinalSummaryResponse` (overall feedback + final score + full history) |
| `error` | server → client | `{ error: string }` |

The full schemas live in `app/schemas.py`.

## Local development

```bash
# Syntax / import sanity check
python -m compileall -q app
```

GitHub Actions runs the same compile pass plus a `ruff check` on every
push. See `.github/workflows/ci.yml`.

## Roadmap

- Persist sessions so a candidate can resume an in-progress interview.
- Surface the per-turn `score_breakdown` as a live chart in `index.html`.
- Add an Anthropic Claude backend alongside the Gemini one and let the
  user pick the model from the UI.
- Cache Whisper model load between sessions.
- Containerize (Dockerfile + healthcheck) so the app deploys behind
  a single `docker run`.
