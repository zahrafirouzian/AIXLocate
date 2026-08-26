from app.models.state import ResearchState

from app.services.llm import ask_llm


def planner_node(state: ResearchState):

    query = state["query"]


    prompt = f"""
You are a data center location planning assistant.

Extract city and criteria from this request:

{query}

Return only the city name.
"""


    city = ask_llm(prompt)


    return {
        "city": city.strip()
    }