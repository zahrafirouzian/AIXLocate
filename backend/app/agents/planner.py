from app.models.state import ResearchState

def planner_node(state: ResearchState):

    query = state["query"]

    city = "Phoenix"

    return {
        "city": city
    }