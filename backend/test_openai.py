from app.services.llm import ask_llm


response = ask_llm(
    "Explain why climate matters for AI data centers in one sentence."
)

print(response)
