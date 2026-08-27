import requests

from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def get_city_boundary(city: str):

    params = {
        "q": city,
        "format": "geojson",
        "polygon_geojson": 1,
        "limit": 1,
    }

    headers = {
        "User-Agent": "AIXLocate/1.0"
    }

    response = requests.get(
        NOMINATIM_URL,
        params=params,
        headers=headers,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("features"):
        raise ValueError(
            f"City boundary not found: {city}"
        )

    geometry = data["features"][0].get("geometry")

    if not geometry:
        raise ValueError(
            f"No geometry found for city: {city}"
        )

    geom = shape(geometry)

    if geom.is_empty:
        raise ValueError(
            f"Empty geometry found for city: {city}"
        )

    # FortyGuard requires Polygon.
    if geom.geom_type == "MultiPolygon":
        geom = geom.convex_hull

    if geom.geom_type != "Polygon":
        raise ValueError(
            f"Unsupported geometry: {geom.geom_type}"
        )

    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "city": city
                },
                "geometry": mapping(geom),
            }
        ],
    }