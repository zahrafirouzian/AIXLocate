from app.models.state import ResearchState


def calculate_score(location):

    temperature_score = max(
        0,
        100 - (location["temperature"] - 30) * 5
    )

    heat_score = 100 - location["heat_stress"]


    final_score = (
        temperature_score * 0.5
        +
        heat_score * 0.5
    )

    return round(final_score, 2)



def scoring_node(state: ResearchState):

    locations = state["locations"]

    scored_locations = []


    for location in locations:

        score = calculate_score(location)

        scored_locations.append(
            {
                **location,
                "score": score
            }
        )


    best = max(
        scored_locations,
        key=lambda x: x["score"]
    )


    return {
        "locations": scored_locations,
        "recommendation": best["name"]
    }