from app.models.state import ResearchState
from app.services.scoring import calculate_suitability


def scoring_node(state: ResearchState):

    locations = state["locations"]

    scored_locations = []

    for location in locations:

        scored = calculate_suitability(location)

        print("\n===== FINAL SCORE =====")
        print("NAME:", location["name"])
        print("TEMPERATURE:", location["temperature"])
        print("SOLAR GHI:", location["solar_ghi"])
        print("CLIMATE SCORE:", location.get("climate_score"))
        print("COOLING:", scored["cooling_score"])
        print("THERMAL:", scored["thermal_score"])
        print("RISK:", scored["risk_score"])
        print("ENVIRONMENTAL:", scored["environmental_score"])
        print("SUITABILITY:", scored["suitability_score"])
        print("=======================\n")

        scored_locations.append(scored)

    best = max(
        scored_locations,
        key=lambda x: x["suitability_score"]
    )

    return {
        "locations": scored_locations,
        "recommendation": best["name"]
    }