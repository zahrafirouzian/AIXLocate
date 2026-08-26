from app.models.state import ResearchState

def location_node(state: ResearchState):

    locations = [
        {
            "name": "North Phoenix",
            "score": 87,
            "reason": "Lower heat stress"
        },
        {
            "name": "Downtown Phoenix",
            "score": 62,
            "reason": "Higher thermal load"
        }
    ]

    return {
        "locations": locations
    }