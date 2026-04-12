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


def generate_questions_from_jd(jd_text: str) -> InterviewQuestionsResponse:
    """
    Analyzes a job description and generates relevant interview questions using Gemini.
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",
                                 temperature=0.3,
                                 convert_system_message_to_human=True)
    
    parser = PydanticOutputParser(pydantic_object=InterviewQuestionsResponse)

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

    # Correct chain: The Pydantic parser will handle the string-to-object conversion
    chain = prompt | model | parser

    print("🧠 Generating interview questions with Gemini...")
    response = chain.invoke({"jd_text": jd_text})
    print("✅ Parsed response received from Gemini.")
    
    return response