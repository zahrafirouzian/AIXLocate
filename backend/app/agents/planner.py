from app.models.state import ResearchState


def planner_node(state: ResearchState):

    city = state["city"].strip()

    if not city:
        raise ValueError("City is required")

    print("Planning analysis for:", city)

    return {
        "city": city
    }