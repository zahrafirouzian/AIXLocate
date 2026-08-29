from typing import List

from shapely.geometry import shape, Point

from app.services.geocoder import get_city_coordinates
from app.services.city_boundary import get_city_boundary


TARGET_CANDIDATES = 5


def geographic_distance(point_a, point_b):
    """
    Approximate geographic distance in degrees.
    Good enough for selecting spatially separated
    candidates within the same city.
    """

    lat1, lon1 = point_a
    lat2, lon2 = point_b

    return (
        (lat1 - lat2) ** 2
        +
        (lon1 - lon2) ** 2
    ) ** 0.5


def generate_candidate_pool(city_polygon, grid_size=15):
    """
    Generate a dense grid of candidate points
    inside the actual city boundary.
    """

    min_lon, min_lat, max_lon, max_lat = (
        city_polygon.bounds
    )

    candidates = []

    lat_step = (
        max_lat - min_lat
    ) / (grid_size - 1)

    lon_step = (
        max_lon - min_lon
    ) / (grid_size - 1)

    for row in range(grid_size):

        lat = min_lat + row * lat_step

        for col in range(grid_size):

            lon = min_lon + col * lon_step

            point = Point(
                lon,
                lat
            )

            if city_polygon.covers(point):

                candidates.append(
                    {
                        "lat": lat,
                        "lon": lon
                    }
                )

    return candidates


def select_diverse_candidates(
    candidates,
    city_polygon,
    target_count=TARGET_CANDIDATES
):
    """
    Select geographically separated candidates.

    Strategy:
    - start from city representative point
    - repeatedly choose the point farthest
      from all already selected points
    """

    if not candidates:
        return []

    representative = (
        city_polygon.representative_point()
    )

    center = (
        representative.y,
        representative.x
    )

    first = min(
        candidates,
        key=lambda candidate: geographic_distance(
            (
                candidate["lat"],
                candidate["lon"]
            ),
            center
        )
    )

    selected = [first]

    remaining = [
        candidate
        for candidate in candidates
        if candidate != first
    ]

    while (
        len(selected) < target_count
        and remaining
    ):

        best_candidate = None
        best_distance = -1

        for candidate in remaining:

            candidate_point = (
                candidate["lat"],
                candidate["lon"]
            )

            min_distance = min(
                geographic_distance(
                    candidate_point,
                    (
                        selected_point["lat"],
                        selected_point["lon"]
                    )
                )
                for selected_point in selected
            )

            if min_distance > best_distance:

                best_distance = min_distance
                best_candidate = candidate

        if best_candidate is None:
            break

        selected.append(
            best_candidate
        )

        remaining.remove(
            best_candidate
        )

    return selected


def get_area_name(
    candidate,
    city_polygon
):
    """
    Give the candidate a relative geographic label.
    """

    representative = (
        city_polygon.representative_point()
    )

    center_lat = representative.y
    center_lon = representative.x

    lat_range = max(
        city_polygon.bounds[3]
        - city_polygon.bounds[1],
        0.000001
    )

    lon_range = max(
        city_polygon.bounds[2]
        - city_polygon.bounds[0],
        0.000001
    )

    lat_ratio = (
        candidate["lat"]
        - center_lat
    ) / lat_range

    lon_ratio = (
        candidate["lon"]
        - center_lon
    ) / lon_range

    # Central
    if (
        abs(lat_ratio) < 0.18
        and abs(lon_ratio) < 0.18
    ):
        return "Central"

    # Prefer dominant direction
    if abs(lat_ratio) >= abs(lon_ratio):

        if lat_ratio > 0:
            return "North"

        return "South"

    if lon_ratio > 0:
        return "East"

    return "West"


def generate_candidates(city: str) -> List[dict]:

    print(
        "\n===== GENERATING SPATIAL CANDIDATES ====="
    )

    print(
        "City:",
        city
    )

    # --------------------------------------------------
    # Get actual city boundary
    # --------------------------------------------------

    boundary = get_city_boundary(
        city
    )

    geometry = (
        boundary["features"][0]["geometry"]
    )

    city_polygon = shape(
        geometry
    )

    if city_polygon.is_empty:
        raise ValueError(
            f"Empty city boundary: {city}"
        )

    # --------------------------------------------------
    # Generate dense pool
    # --------------------------------------------------

    candidate_pool = (
        generate_candidate_pool(
            city_polygon,
            grid_size=15
        )
    )

    print(
        "Candidate pool:",
        len(candidate_pool)
    )

    if not candidate_pool:
        raise ValueError(
            f"No candidate locations found inside {city}"
        )

    # --------------------------------------------------
    # Select geographically diverse points
    # --------------------------------------------------

    selected = (
        select_diverse_candidates(
            candidate_pool,
            city_polygon,
            TARGET_CANDIDATES
        )
    )

    if len(selected) < TARGET_CANDIDATES:
        raise ValueError(
            f"Could only generate "
            f"{len(selected)} candidates for {city}"
        )

    # --------------------------------------------------
    # Name locations
    # --------------------------------------------------

    locations = []

    used_names = set()

    for index, candidate in enumerate(selected):

        area_name = get_area_name(
            candidate,
            city_polygon
        )

        if area_name in used_names:

            area_name = (
                f"Area {index + 1}"
            )

        used_names.add(
            area_name
        )

        locations.append(
            {
                "name": f"{area_name} {city}",

                "lat": round(
                    candidate["lat"],
                    6
                ),

                "lon": round(
                    candidate["lon"],
                    6
                )
            }
        )

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    print(
        "\n===== SELECTED CANDIDATES ====="
    )

    for location in locations:

        print(
            f"{location['name']} | "
            f"LAT: {location['lat']} | "
            f"LON: {location['lon']}"
        )

    print(
        "Total:",
        len(locations)
    )

    print(
        "===============================\n"
    )

    return locations