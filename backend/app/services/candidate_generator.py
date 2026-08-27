from typing import List
from app.services.geocoder import get_city_coordinates


def generate_candidates(city: str) -> List[dict]:

    lat, lon = get_city_coordinates(city)

    return [

        {
            "name": f"North {city}",
            "lat": lat + 0.15,
            "lon": lon,
        },

        {
            "name": f"South {city}",
            "lat": lat - 0.15,
            "lon": lon,
        },

        {
            "name": f"East {city}",
            "lat": lat,
            "lon": lon + 0.15,
        },

        {
            "name": f"West {city}",
            "lat": lat,
            "lon": lon - 0.15,
        },

        {
            "name": f"Downtown {city}",
            "lat": lat,
            "lon": lon,
        }

    ]