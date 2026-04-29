# AI Interview Coach

An AI-powered mock-interview practice tool. Upload a job description PDF, get
role-specific questions read aloud, answer in your own voice, and receive
structured feedback on every answer plus a final overall summary.

The whole interview runs over a single WebSocket so the experience is
turn-by-turn and low-latency: question audio in, answer audio out,
evaluation back in real time.

## Features

- **Job-description aware questions.** A LangChain agent reads the JD PDF
  text and generates a tailored interview question set.
- **Spoken questions.** Each question is rendered to MP3 with `gTTS` and
  streamed to the browser as base64.
- **Spoken answers.** The browser captures microphone audio and sends it
  back; OpenAI Whisper transcribes it server-side.
- **Structured evaluation per turn.** Every answer is scored 1–10 on
  `relevance`, `clarity`, and `impact`, with constructive written feedback
  (typed via Pydantic in `app/schemas.py`).
- **Final interview summary.** When the question list is exhausted, a
  summary agent produces overall feedback, an averaged score, and the full
  question/answer history.
- **Single-page web UI.** `index.html` ships the entire frontend—no build
  step required.

## Architecture

```
Browser (index.html, mic + audio playback)
   │
   │  WebSocket /ws/interview
   ▼
FastAPI app (app/main.py)
   ├─ app/utils/document_parser.py    PDF → text via pypdf
   ├─ app/agents/question_generator.py JD text → InterviewQuestionsResponse
   ├─ app/agents/answer_evaluator.py   audio + JD + Q → EvaluationResponse
   │     └─ OpenAI Whisper (transcription)
   │     └─ LangChain + langchain-openai (scoring + feedback)
   └─ app/agents/summary_generator.py history → FinalSummaryResponse
gTTS → MP3 bytes for question playback
```

Response schemas (see `app/schemas.py`):

- `InterviewQuestionsResponse` → list of generated questions
- `EvaluationResponse` → `transcribed_text`, `feedback`, `total_score`,
  `score_breakdown { relevance, clarity, impact }`
- `FinalSummaryResponse` → `overall_feedback`, `final_score`,
  `full_history`

## Tech stack

- **Backend:** FastAPI, WebSockets, Pydantic v2
- **LLM:** OpenAI via `langchain-openai`
- **Speech-to-text:** `openai-whisper` (local model)
- **Text-to-speech:** `gTTS`
- **PDF parsing:** `pypdf`
- **Vector store:** `faiss-cpu` (reserved for retrieval extensions)
- **Frontend:** plain HTML + JS (`index.html`)

## Quick start

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env        # then set OPENAI_API_KEY

uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000` in a browser. Allow microphone access when
prompted, upload a job description PDF, and the interview begins.

> **System dependency:** OpenAI Whisper requires `ffmpeg` to be installed and
> on your `PATH`.
>
> - macOS: `brew install ffmpeg`
> - Ubuntu/Debian: `sudo apt-get install ffmpeg`
> - Windows: <https://ffmpeg.org/download.html>

## Configuration

All runtime configuration is driven by environment variables loaded via
`python-dotenv`. See `.env.example` for the full list.

| Variable | Required | Default | Purpose |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes | — | Auth for the LLM scoring + summary agents |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Override the chat model |
| `WHISPER_MODEL` | No | `base` | Whisper checkpoint (`tiny`/`base`/`small`/`medium`/`large`) |
| `TTS_LANG` | No | `en` | gTTS language code |

## WebSocket protocol

Client connects to `/ws/interview`, then:

1. Sends raw bytes of the JD PDF.
2. Receives a JSON `WebSocketMessage` of `type="question"` with
   `data.text` and base64 `data.audio` for each question.
3. For each question, sends raw bytes of the recorded answer audio.
4. Receives a `WebSocketMessage` of `type="evaluation"` with the
   `EvaluationResponse` payload.
5. After the last question, receives a `WebSocketMessage` of
   `type="final_summary"` with the `FinalSummaryResponse` payload.

Errors are sent as `WebSocketError { error: string }` and the connection is
closed.

## Project layout

```
.
├─ app/
│  ├─ main.py                   FastAPI + WebSocket interview loop
│  ├─ schemas.py                Pydantic response/error models
│  ├─ agents/
│  │  ├─ question_generator.py  JD → questions
│  │  ├─ answer_evaluator.py    audio + Q + JD → scored feedback
│  │  └─ summary_generator.py   transcript → final summary
│  └─ utils/
│     └─ document_parser.py     PDF → plain text
├─ index.html                   single-page frontend
├─ requirements.txt             Python dependencies
├─ .env.example                 env-var template
└─ LICENSE                      MIT
```

## Roadmap

- Persist sessions (transcript + audio) for later review.
- Add a retrieval layer (`faiss-cpu` already pinned) so questions can be
  grounded in the candidate's own resume.
- Switch the LLM provider to a local OSS model behind the same LangChain
  interface for offline use.
- Add automated tests (`pytest`) and a CI workflow.

## License

MIT — see [`LICENSE`](LICENSE).
