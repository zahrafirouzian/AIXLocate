from app.models.state import ResearchState

def scoring_node(state: ResearchState):

    locations = state["locations"]

    best = max(
        locations,
        key=lambda x: x["score"]
    )

    return {
        "recommendation": best["name"]
    }