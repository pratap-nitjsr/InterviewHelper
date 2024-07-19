import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferWindowMemory
import PyPDF2

# Load environment variables
load_dotenv()

# Initialize the memory with a buffer for the last 5 conversations
memory = ConversationBufferWindowMemory(k=5, input_key="response")

# Get the API key from environment variables
GEMINI_API = os.getenv("GEMINI_API")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-1.0-pro", google_api_key=GEMINI_API)

# Define the template for generating a reply to an interview question
reply_generation_prompt = PromptTemplate(
    input_variables=["question", "job_role", "interview_stage", "applicant_info"],
    template="""
    Question: {question}
    You are an intellectual and exceptional candidate interviewing for the role of {job_role}.
    You have provided the following information for this position: {applicant_info}
    This is the {interview_stage} round of the interview.
    Based on the above question, formulate a highly impressive answer.
    Ensure that the reply is engaging and does not appear AI-generated.
    Your response must conatin the reply as a candidate only.
    """
)

# Create a chain for generating the reply
reply_chain = LLMChain(
    llm=llm,
    prompt=reply_generation_prompt,
    output_key="generated_reply",
    verbose=True
)

# Define the template for evaluating and refining the generated reply
reply_evaluation_prompt = PromptTemplate(
    input_variables=["interview_stage", "job_role", "generated_reply"],
    template="""
    You are an expert in English grammar and writing. Here is a reply to an interview question
    for the {interview_stage} round of the interview for the role of {job_role}.
    Also ensure that it contains only the reply, not any other unnecessary information.
    If the reply does not meet high standards, update it to ensure it looks authentic and polished.
    Reply: {generated_reply}

    Expert evaluation and refinement of the above reply:
    """
)

# Create a chain for evaluating and refining the reply
review_chain = LLMChain(
    llm=llm,
    prompt=reply_evaluation_prompt,
    output_key="final_reply",
    verbose=True
)

# Combine the generation and evaluation chains into a sequential chain
generate_evaluate_chain = SequentialChain(
    chains=[reply_chain, review_chain],
    input_variables=["question", "job_role", "interview_stage", "applicant_info"],
    output_variables=["generated_reply", "final_reply"],
    verbose=True
)
