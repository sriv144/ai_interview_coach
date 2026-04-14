import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from ..schemas import InterviewQuestionsResponse

load_dotenv()

# Configure Google Generative AI
import google.generativeai as genai
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY not found in .env file")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_questions_from_jd(jd_text: str, resume_text: str = "") -> InterviewQuestionsResponse:
    """
    Analyzes a job description and optionally a resume to generate relevant interview questions using Gemini.
    If resume_text is provided, generates personalized questions that probe experience gaps and specific skills.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                 temperature=0.3,
                                 convert_system_message_to_human=True)

    parser = PydanticOutputParser(pydantic_object=InterviewQuestionsResponse)

    if resume_text.strip():
        prompt_template = """
        You are an expert hiring manager for a top-tier tech company.
        Your task is to analyze the following job description AND the candidate's resume to generate 5 highly personalized interview questions.

        Focus on:
        1. Probing experience gaps between the candidate's background and the role requirements
        2. Diving deep into the candidate's specific skills mentioned in their resume as they relate to the JD
        3. Asking about their most relevant projects and how they solve problems similar to those the role requires
        4. Uncovering their growth areas and willingness to learn

        Job Description:
        ---
        {jd_text}
        ---

        Candidate's Resume:
        ---
        {resume_text}
        ---

        Please provide your output ONLY as a valid JSON object, following this structure:
        {format_instructions}

        Do not include any other text or markdown formatting like ```json before or after the JSON object.
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["jd_text", "resume_text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        print("🧠 Generating personalized interview questions with Gemini (with resume context)...")
        response = chain.invoke({"jd_text": jd_text, "resume_text": resume_text})
    else:
        prompt_template = """
        You are an expert hiring manager for a top-tier tech company.
        Your task is to analyze the following job description and generate 5 relevant interview questions.

        Job Description:
        ---
        {jd_text}
        ---

        Please provide your output ONLY as a valid JSON object, following this structure:
        {format_instructions}

        Do not include any other text or markdown formatting like ```json before or after the JSON object.
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["jd_text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        print("🧠 Generating interview questions with Gemini...")
        response = chain.invoke({"jd_text": jd_text})

    print("✅ Parsed response received from Gemini.")

    return response