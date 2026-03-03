import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

print("DEBUG KEY:", os.getenv("OPENROUTER_API_KEY"))

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables.")

    return ChatOpenAI(
        model="openai/gpt-4o-mini",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0,
    )