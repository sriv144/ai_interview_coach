# AI Interview Coach

> Real-time, AI-powered mock interviews. Upload a job description, get a
> personalized question set, answer with your voice, and receive structured
> feedback — all streamed over a single WebSocket connection.

[![CI](https://github.com/sriv144/ai_interview_coach/actions/workflows/ci.yml/badge.svg)](https://github.com/sriv144/ai_interview_coach/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

## Why

Generic interview-prep apps ask cookie-cutter questions. AI Interview Coach
reads the target job description, generates role-specific questions,
transcribes voice answers with Whisper, scores each response on relevance,
clarity and impact, then synthesizes an end-of-interview summary that
highlights strengths and gaps.

## Features

- **JD-aware question generation** — agents extract requirements from an
  uploaded PDF job description and produce a tailored question set.
- **Voice in, voice out** — the browser captures audio, the server replies
  with TTS-rendered questions via gTTS for a natural cadence.
- **Per-answer scoring** — Whisper transcription plus LLM evaluation
  returns a 1–10 score broken out across relevance / clarity / impact.
- **Final interview summary** — once every question is answered, an
  aggregate feedback report and overall score are streamed back.
- **WebSocket-first architecture** — a single `/ws/interview` channel
  multiplexes the PDF upload, audio frames, evaluations, and summaries.

## Architecture

```text
Browser (index.html)
   |  WebSocket: binary JD PDF + audio frames, JSON results
   v
FastAPI app (app/main.py, /ws/interview)
   |--- parse_pdf_to_text       PDF bytes -> JD text
   |--- generate_questions_from_jd  JD text -> List[Question]
   |--- evaluate_answer         Whisper transcribe + LLM scoring
   '--- generate_final_summary  aggregate score + feedback
```

Each agent in `app/agents/` is a thin LangChain pipeline over the configured
LLM provider. Pydantic schemas in `app/schemas.py` validate every payload
that crosses the WebSocket.

## Quick start

```bash
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env               # then edit and add OPENAI_API_KEY
python -m uvicorn app.main:app --reload --port 8000
```

Open <http://localhost:8000> and upload a job-description PDF to start the
interview.

## Environment

| Variable | Required | Notes |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | Used by `langchain-openai` for question generation and answer evaluation. |
| `WHISPER_MODEL`  | No  | Whisper model size (`tiny` / `base` / `small` / `medium` / `large`). Default: `base`. |

See [`.env.example`](./.env.example) for the full template.

## Tech stack

- **API**: FastAPI, WebSockets, Pydantic v2
- **LLM orchestration**: LangChain (`langchain-openai`)
- **Speech-to-text**: OpenAI Whisper (runs locally)
- **Text-to-speech**: gTTS
- **Document parsing**: pypdf
- **Vector store (planned)**: FAISS

## Repository layout

```text
app/
  main.py             FastAPI app + /ws/interview entrypoint
  schemas.py          Pydantic models for the wire protocol
  agents/             question_generator, answer_evaluator, summary_generator
  utils/              document_parser (PDF -> text)
index.html            Single-page client (audio capture + WS)
requirements.txt      Python dependencies
.env.example          Environment template
```

## Roadmap

- Configurable LLM provider (OpenAI / Anthropic / local).
- Persistent interview history per user with a queryable transcript store.
- Resume + JD cross-referencing for personalized prep paths.
- Containerized deployment (Dockerfile + docker-compose).
- Streaming partial transcripts to the client during long answers.

## License

[MIT](./LICENSE) © sriv144
