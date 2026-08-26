from app.services.llm import ask_llm


result = ask_llm(
    "Explain why cooling efficiency is important for AI data centers."
)

print(result)
