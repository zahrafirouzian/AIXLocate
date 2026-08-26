from fastapi import APIRouter

from app.graph.workflow import graph


router = APIRouter()


@router.post("/analyze")
def analyze(data: dict):

    result = graph.invoke(data)


    locations = result.get(
        "locations",
        []
    )


    recommendation = result.get(
        "recommendation"
    )


    best_location = None


    for loc in locations:

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


        "locations": locations

    }