from src.core.llm import get_llm

llm = get_llm()

response = llm.invoke("Hi qwen i am using you on my hackathon")
print(response.content) 