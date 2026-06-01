# AI Interview Coach

A real-time, voice-driven mock interview platform. Upload a job description as a PDF, and the app generates tailored interview questions, asks them via text-to-speech, transcribes your spoken answers with Whisper, scores each response on relevance / clarity / impact, and delivers a final performance summary — all streamed over a single WebSocket.

## Why this exists

Generic interview practice tools ignore the actual role you're targeting. AI Interview Coach reads the JD you upload and personalizes the entire session: question selection, evaluation rubric, and the final coaching summary are all grounded in that specific job's requirements.

## Features

- **JD-aware question generation** — parses an uploaded PDF and uses an LLM to produce role-specific behavioral and technical questions.
- **Voice in, voice out** — questions are spoken via gTTS; answers are recorded in the browser, sent over WebSocket, and transcribed with OpenAI Whisper.
- **Structured scoring** — every answer is graded on three axes (relevance, clarity, impact) on a 1–10 scale, with written feedback and a weighted total.
- **Final coaching summary** — after the last question, a summary agent reviews the full transcript and returns overall feedback, a final score, and the full history.
- **Streaming WebSocket protocol** — one duplex connection drives the whole interview: JD upload, question audio, answer audio, per-turn evaluation, and final summary.
- **Typed contracts end-to-end** — Pydantic schemas (`InterviewQuestion`, `EvaluationResponse`, `ScoreBreakdown`, `FinalSummaryResponse`) guarantee the LLM output, the WebSocket envelope, and the browser stay in lock-step.

## Architecture

```
  Browser (index.html)
      |
      |  WebSocket  /ws/interview
      v
  FastAPI  (app/main.py)
      |
      +-- parse_pdf_to_text   (app/utils)
      +-- question_generator  (LangChain LLM)  -> InterviewQuestionsResponse
      +-- gTTS                                  -> question audio (base64)
      +-- answer_evaluator    (Whisper + LLM)  -> EvaluationResponse
      +-- summary_generator   (LangChain LLM)  -> FinalSummaryResponse
```

Four message types flow over the socket: `question`, `evaluation`, `final_summary`, and `error`. Each is wrapped in a `WebSocketMessage` envelope.

## Tech stack

| Layer        | Stack                                                              |
|--------------|---------------------------------------------------------------------|
| Backend      | FastAPI, Uvicorn, WebSockets                                       |
| LLM          | LangChain + `langchain-openai` (structured output via Pydantic)    |
| Speech       | `openai-whisper` (STT), `gTTS` (TTS)                                |
| Documents    | `pypdf` for JD parsing                                              |
| Vector store | `faiss-cpu` (scaffolding for retrieval-augmented variants)          |
| Frontend     | Single-page `index.html` (vanilla JS, MediaRecorder API)            |

## Project layout

```
app/
  main.py                 FastAPI app + /ws/interview WebSocket loop
  schemas.py              Pydantic models for every message and LLM output
  agents/
    question_generator.py Generates JD-tailored questions
    answer_evaluator.py   Transcribes audio + scores the answer
    summary_generator.py  Builds the final coaching summary
  utils/                  PDF parsing helpers
index.html                Browser client (record / playback / display)
requirements.txt          Python dependencies
.env.example              Required environment variables
```

## Quick start

```bash
# 1. Clone and enter the repo
git clone https://github.com/sriv144/ai_interview_coach.git
cd ai_interview_coach

# 2. Create a virtualenv
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# then edit .env and set OPENAI_API_KEY

# 5. Run the app
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in a modern browser (Chrome / Edge recommended for `MediaRecorder` support), upload a PDF of the target job description, and start the interview.

> **Whisper note:** the first answer evaluation downloads the Whisper model weights to your local cache. Expect a one-time delay (a few hundred MB) on first use.

## End-to-end flow

1. **Client uploads JD** — the browser sends the PDF bytes over the WebSocket. The server parses it to text.
2. **Server generates questions** — `question_generator` returns a typed list of `InterviewQuestion`s.
3. **Per-question loop**:
   - Server speaks the question with gTTS and sends `{ type: "question", data: { text, audio } }`.
   - Client records an audio answer and sends the bytes back.
   - Server transcribes with Whisper, scores with the LLM, and sends `{ type: "evaluation", data: EvaluationResponse }`.
4. **Final summary** — once all questions are answered, the server sends `{ type: "final_summary", data: FinalSummaryResponse }` with the full history.
5. **Errors** are surfaced as `{ type: "error", data: WebSocketError }` and the connection is closed cleanly.

## Scoring rubric

Each answer is scored 1–10 on three dimensions:

| Dimension  | What it measures                                                  |
|------------|--------------------------------------------------------------------|
| Relevance  | How well the answer addresses the JD and the specific question.   |
| Clarity    | How clear, concise, and well-structured the answer is.            |
| Impact     | Whether the answer cites concrete examples and quantified outcomes.|

The `total_score` is a weighted blend exposed back to the UI alongside written feedback.

## Environment variables

See `.env.example` for the full list. Minimum required:

| Variable          | Required | Description                                |
|-------------------|----------|--------------------------------------------|
| `OPENAI_API_KEY`  | Yes      | Used by `langchain-openai` and Whisper API |

## Roadmap

- Swap gTTS for a streaming, lower-latency TTS provider.
- Retrieval-augmented question generation backed by the `faiss-cpu` scaffolding (industry-specific question banks).
- Resume-aware mode: combine JD + resume to produce tailored "tell me about a time" questions.
- Per-question hints + retry mode for practice without scoring penalties.
- Persisted session history + an analytics dashboard across multiple mock interviews.

## Contributing

Pull requests are welcome. Please open an issue first for substantial changes so we can align on direction.

## License

MIT — see `LICENSE` if present, otherwise feel free to fork and adapt.
