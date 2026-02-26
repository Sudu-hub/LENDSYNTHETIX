from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(model="qwen2:1.5b",temperature=0)