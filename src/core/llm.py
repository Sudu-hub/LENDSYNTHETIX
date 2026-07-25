import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load .env
load_dotenv()


def get_llm():

    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found in environment variables."
        )

    return ChatOpenAI(
        model="openai/gpt-4o-mini",

        # OpenRouter API key
        api_key=api_key,

        # OpenRouter endpoint
        base_url="https://openrouter.ai/api/v1",

        # Keep responses deterministic
        temperature=0,

        # IMPORTANT:
        # Prevent OpenRouter from requesting 16384 tokens
        max_tokens=2000,

        # Optional OpenRouter headers
        default_headers={
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "LendSynthetix - Digital AI Credit War Room",
        },
    )