import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from typing import List
from ..schemas import InterviewTurn, FinalSummaryResponse

load_dotenv()

def generate_final_summary(job_description_text: str, interview_history: List[InterviewTurn]) -> FinalSummaryResponse:
    """
    Analyzes the entire interview history and generates a final summary.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                 temperature=0.5,
                                 convert_system_message_to_human=True)
    
    parser = PydanticOutputParser(pydantic_object=FinalSummaryResponse)

    # Convert the history to a nicely formatted string for the prompt
    history_string = ""
    total_score = 0
    for i, turn in enumerate(interview_history):
        history_string += f"--- Question {i+1} ---\n"
        history_string += f"Question: {turn.question}\n"
        history_string += f"Candidate's Answer: {turn.evaluation.transcribed_text}\n"
        history_string += f"Feedback: {turn.evaluation.feedback}\n"
        history_string += f"Score: {turn.evaluation.total_score}/10\n\n"
        total_score += turn.evaluation.total_score
    
    final_average_score = round(total_score / len(interview_history), 2)


    prompt_template = """
    You are an expert career coach providing a final summary of a candidate's mock interview performance.
    Analyze the entire interview history provided below, considering the initial job description.

    JOB DESCRIPTION:
    ---
    {jd_text}
    ---

    FULL INTERVIEW HISTORY:
    ---
    {interview_history}
    ---

    INSTRUCTIONS:
    1.  **Overall Feedback:** Write a comprehensive summary (2-3 paragraphs) of the candidate's performance. Start by highlighting their key strengths demonstrated across multiple answers. Then, identify 1-2 overarching areas for improvement. Be constructive and encouraging.
    2.  **Final Score:** Use the pre-calculated final average score: {final_score}.
    3.  **Full History:** Include the complete, unmodified interview history in your output.

    Your output MUST be a valid JSON object that strictly adheres to the provided format instructions.
    {format_instructions}
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["jd_text", "interview_history", "final_score"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | model | parser

    print("🧠 Generating final interview summary...")
    response = chain.invoke({
        "jd_text": job_description_text,
        "interview_history": history_string,
        "final_score": final_average_score
    })
    print("✅ Final summary complete.")
    
    return response