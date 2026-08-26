from app.models.state import ResearchState

from app.services.llm import ask_llm



def report_node(state: ResearchState):

    location = state["recommendation"]

    locations = state["locations"]


    prompt = f"""
You are an AI infrastructure consultant.

Explain why this location is recommended:

Location:
{location}

Data:
{locations}

Write a short professional recommendation.
"""


    report = ask_llm(prompt)


    return {
        "report": report
    }