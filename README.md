# AI Interview Coach

A FastAPI-backed AI interview prep platform with a single-page web UI. Upload a job description, get a sequence of role-tailored questions, answer them by voice, and receive structured per-answer feedback plus a final summary report.

## Highlights

- **JD-driven question generation.** Parses an uploaded job-description PDF and asks an LLM to produce a focused set of behavioural and technical questions.
- **Voice-in, voice-out loop.** Questions are spoken back via Google text-to-speech; answers are sent as audio over a WebSocket and transcribed for evaluation.
- **Structured per-answer feedback.** Each answer is scored and accompanied by a written critique returned to the UI as soon as the answer is complete.
- **Final summary report.** When the question list is exhausted, the agent generates an end-of-interview summary grounded in the full evaluation history.
- **Pure WebSocket protocol.** All interaction with the backend flows through a single `/ws/interview` channel, so the browser UI never needs to long-poll.

## Tech Stack

- **Backend:** FastAPI, uvicorn, websockets
- **LLM orchestration:** LangChain (OpenAI-compatible chat models)
- **Document parsing:** pypdf
- **Speech:** OpenAI Whisper for transcription, gTTS for spoken question playback
- **Frontend:** static `index.html` served from FastAPI (no build step)

## Project Structure

```text
app/
  main.py                 FastAPI app + /ws/interview WebSocket loop
  schemas.py              Pydantic message schemas (questions, evaluations, summary)
  agents/
    question_generator.py LLM prompt for JD-to-question generation
    answer_evaluator.py   LLM prompt for per-answer scoring + critique
    summary_generator.py  LLM prompt for the end-of-interview summary
  utils/                  PDF parsing helpers
index.html                Single-page browser UI
requirements.txt          Python dependencies
.env.example              Environment variable template
```

## Requirements

- Python 3.10 or newer
- An OpenAI-compatible chat model API key (configured in `.env`)
- A working microphone and a modern browser for the recording flow

## Quick Start

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env       # then edit .env and add your API key
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` in your browser, upload a job description PDF, allow microphone access, and start the interview.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `OPENAI_API_KEY` | Yes | API key for the chat model used by the LangChain pipelines |

The full template lives in `.env.example`.

## Interview Flow

1. Browser opens a WebSocket to `/ws/interview` and uploads the JD PDF as bytes.
2. Backend parses the PDF and asks the question-generation agent to produce a question list.
3. For each question:
   - The backend speaks the question with gTTS and sends `{type: "question", data: {text, audio}}`.
   - The browser records and uploads the answer as audio bytes.
   - The answer evaluator transcribes the audio and returns a structured `evaluation` payload.
4. After the final question, the summary generator produces a `final_summary` payload covering strengths, gaps, and recommended follow-up topics.

## Roadmap

- Persist completed sessions so candidates can revisit feedback later.
- Add a question-bank fallback when no JD is uploaded (e.g. by target role).
- Expose model and voice choices as runtime settings instead of code defaults.
- Add an automated test layer around the agent prompts and the WebSocket protocol.
