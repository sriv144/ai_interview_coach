# In app/agents/answer_evaluator.py

import os
import tempfile
import whisper
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from ..schemas import EvaluationResponse

# Load the Whisper model once when the module is loaded
whisper_model = whisper.load_model("base")

def evaluate_answer(
    audio_file: bytes,
    job_description_text: str,
    question_text: str
) -> EvaluationResponse:
    
    temp_audio_path = None
    try:
        # --- Speech-to-Text using Whisper (Corrected Method) ---
        print("🎤 Transcribing audio...")
        
        # 1. Create a named temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio_file:
            temp_audio_file.write(audio_file)
            temp_audio_path = temp_audio_file.name

        # 2. The 'with' block is now finished, so the file is closed and the lock is released.
        #    Now, we pass the file path to Whisper.
        result = whisper_model.transcribe(temp_audio_path)
        transcribed_text = result["text"]
        print(f"✅ Transcription complete: \"{transcribed_text}\"")

    finally:
        # 3. Ensure the temporary file is deleted, even if an error occurs
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.unlink(temp_audio_path)

    # --- LLM-based Evaluation (This part remains the same) ---
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                 temperature=0.3,
                                 convert_system_message_to_human=True)
    
    parser = PydanticOutputParser(pydantic_object=EvaluationResponse)

    prompt_template = """
    You are an expert interview coach for a top-tier tech company.
    Your task is to evaluate a candidate's answer to an interview question based on the provided job description.

    JOB DESCRIPTION:
    ---
    {jd_text}
    ---

    INTERVIEW QUESTION:
    "{question}"

    CANDIDATE'S ANSWER:
    "{answer}"

    EVALUATION INSTRUCTIONS:
    - You must score the answer on three criteria: relevance, clarity, and impact, each on a scale of 1 to 10.
    - **Relevance:** How well does the answer relate to the skills and responsibilities in the job description? (Score 1-10)
    - **Clarity:** How clear, concise, and easy to understand was the answer? (Score 1-10)
    - **Impact:** Did the candidate use strong examples and demonstrate the impact of their work? (Score 1-10)
    - **Total Score:** Calculate a weighted total score using this exact formula: (Relevance * 0.5) + (Clarity * 0.25) + (Impact * 0.25). The result can be a float.
    - **Feedback:** Provide specific, constructive feedback. Start with something positive, then suggest 1-2 concrete areas for improvement.
    - **Transcribed Text:** Include the original transcribed text in your final output.

    Your output MUST be a valid JSON object that strictly adheres to the provided format instructions.
    {format_instructions}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["jd_text", "question", "answer"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    print("🧠 Evaluating answer...")
    response = chain.invoke({
        "jd_text": job_description_text,
        "question": question_text,
        "answer": transcribed_text,
    })
    print("✅ Evaluation complete.")
    
    return response