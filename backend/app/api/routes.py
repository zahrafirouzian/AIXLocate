from fastapi import APIRouter

from app.graph.workflow import graph
from app.services.candidate_generator import generate_candidates


router = APIRouter()


@router.post("/analyze")
def analyze(data: dict):

    city = data.get(
        "city",
        "Phoenix"
    )

    locations = generate_candidates(
        city
    )

    result = graph.invoke(
        {
            "query": data["query"],
            "locations": locations,
            "recommendation": None,
            "report": None,
        }
    )

    analyzed_locations = result.get(
        "locations",
        []
    )

    recommendation = result.get(
        "recommendation"
    )

    best_location = None

    for loc in analyzed_locations:

        if loc["name"] == recommendation:

            best_location = {

                "name": loc["name"],

                "score": loc["suitability_score"],

                "temperature": loc["temperature"],

                "solar_ghi": loc["solar_ghi"],

                "solar_dni": loc["solar_dni"]

            }

            break

    return {

        "best_location": best_location,

        "analysis": {

            "report": result.get(
                "report"
            )

        },

        "locations": analyzed_locations

    }