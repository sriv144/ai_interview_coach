import io
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

# Import schemas
from app.schemas import (
    WebSocketMessage,
    WebSocketError,
    InterviewTurn # NEW
)

# Import agent and utility functions
from app.agents.question_generator import generate_questions_from_jd
from app.agents.answer_evaluator import evaluate_answer
from app.agents.summary_generator import generate_final_summary # NEW
from app.utils.document_parser import parse_pdf_to_text
from gtts import gTTS

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.websocket("/ws/interview")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("INFO:     Connection open")
    
    interview_history = [] # NEW: To store the interview turns

    try:
        # 1. Get the Job Description
        jd_bytes = await websocket.receive_bytes()
        jd_text = parse_pdf_to_text(io.BytesIO(jd_bytes))

        if not jd_text:
            error_msg = WebSocketError(error="Could not parse the PDF.")
            await websocket.send_json(error_msg.model_dump())
            return

        # 2. Prompt for Resume (optional)
        await websocket.send_json(WebSocketMessage(type="status", data={"text": "Upload your resume PDF (or send empty bytes to skip)"}).model_dump())

        # 3. Get the Resume (if provided)
        resume_bytes = await websocket.receive_bytes()
        resume_text = ""
        if len(resume_bytes) > 0:
            resume_text = parse_pdf_to_text(io.BytesIO(resume_bytes))
            if resume_text:
                print("✅ Resume parsed successfully.")
            else:
                print("⚠️ Could not parse resume PDF, proceeding without it.")
        else:
            print("ℹ️ No resume provided, generating generic questions.")

        # 4. Generate Questions
        question_response = generate_questions_from_jd(jd_text, resume_text)
        questions = question_response.questions
        question_index = 0

        # 5. Start the Interview Loop
        while question_index < len(questions):
            current_question = questions[question_index].question
            
            tts = gTTS(current_question, lang='en')
            with io.BytesIO() as audio_fp:
                tts.write_to_fp(audio_fp)
                audio_fp.seek(0)
                audio_bytes = audio_fp.read()
            
            question_data = {
                "text": current_question,
                "audio": base64.b64encode(audio_bytes).decode('utf-8')
            }
            await websocket.send_json(WebSocketMessage(type="question", data=question_data).model_dump())
            
            audio_answer_bytes = await websocket.receive_bytes()
            
            evaluation = evaluate_answer(
                audio_file=audio_answer_bytes,
                job_description_text=jd_text,
                question_text=current_question
            )
            
            # Send immediate feedback for the current question
            await websocket.send_json(WebSocketMessage(type="evaluation", data=evaluation.model_dump()).model_dump())
            
            # NEW: Store this turn in our history
            interview_history.append(InterviewTurn(question=current_question, evaluation=evaluation))

            question_index += 1

        # 6. End of Loop - Generate and Send Final Summary
        final_summary = generate_final_summary(
            job_description_text=jd_text,
            interview_history=interview_history
        )
        
        await websocket.send_json(WebSocketMessage(type="final_summary", data=final_summary.model_dump()).model_dump())
        
        # We can now remove the old simple "end" message
        # end_message = "Great job! The interview is now complete. Feel free to review your feedback."
        # await websocket.send_json(WebSocketMessage(type="end", data={"text": end_message}).model_dump())

    except WebSocketDisconnect:
        print("INFO:     Client disconnected")
    except Exception as e:
        print(f"An error occurred in the WebSocket: {e}")
        error_msg = WebSocketError(error=f"An unexpected server error occurred: {str(e)}")
        if websocket.client_state.name == 'CONNECTED':
            await websocket.send_json(error_msg.model_dump())
    finally:
        if websocket.client_state.name == 'CONNECTED':
            await websocket.close()
        print("INFO:     Connection closed")