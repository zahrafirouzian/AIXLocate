from app.models.state import ResearchState

from app.services.scoring import calculate_suitability



def scoring_node(state: ResearchState):

    locations = state["locations"]


    scored_locations = []


    for location in locations:

        scored = calculate_suitability(location)

        scored_locations.append(scored)



    best = max(
        scored_locations,
        key=lambda x:x["suitability_score"]
    )


    return {
        "locations": scored_locations,
        "recommendation": best["name"]
    }