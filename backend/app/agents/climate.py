from app.models.state import ResearchState

from app.tools.fortyguard_heatmap import get_heatmap


def climate_node(state: ResearchState):

    city = state["city"]

    climate_data = get_heatmap(city)


    return {
        "locations": climate_data
    }