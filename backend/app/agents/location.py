from math import sqrt

from shapely.geometry import (
    shape,
    Point
)

from app.models.state import ResearchState

from app.services.city_boundary import (
    get_city_boundary
)


# --------------------------------------------------
# Candidate configuration
# --------------------------------------------------

TARGET_CANDIDATES = 5

GRID_SIZE = 9


# --------------------------------------------------
# Distance between two geographic points
# --------------------------------------------------

def geographic_distance(
    point_a,
    point_b
):

    lat1, lon1 = point_a
    lat2, lon2 = point_b

    return sqrt(
        (lat1 - lat2) ** 2
        +
        (lon1 - lon2) ** 2
    )


# --------------------------------------------------
# Generate candidate grid inside city boundary
# --------------------------------------------------

def generate_candidate_pool(
    city_polygon
):

    min_lon, min_lat, max_lon, max_lat = (
        city_polygon.bounds
    )

    candidates = []

    lat_step = (
        max_lat - min_lat
    ) / (GRID_SIZE - 1)

    lon_step = (
        max_lon - min_lon
    ) / (GRID_SIZE - 1)

    for row in range(GRID_SIZE):

        lat = (
            min_lat
            +
            row * lat_step
        )

        for col in range(GRID_SIZE):

            lon = (
                min_lon
                +
                col * lon_step
            )

            point = Point(
                lon,
                lat
            )

            # Only points covered by the
            # actual city polygon.
            if city_polygon.covers(point):

                candidates.append(
                    {
                        "lat": lat,
                        "lon": lon,
                    }
                )

    return candidates


# --------------------------------------------------
# Select spatially diverse candidates
# --------------------------------------------------

def select_diverse_candidates(
    candidates,
    target_count=TARGET_CANDIDATES
):

    if not candidates:
        return []

    # --------------------------------------------------
    # First point:
    # representative point guaranteed to be
    # inside the polygon.
    #
    # We select the closest grid candidate to it.
    # --------------------------------------------------

    # Candidates are already spatially distributed.
    #
    # Start with the first candidate, then use a
    # greedy max-distance strategy.
    # --------------------------------------------------

    selected = [
        candidates[0]
    ]

    remaining = [
        candidate
        for candidate in candidates
        if candidate is not candidates[0]
    ]

    while (
        len(selected) < target_count
        and remaining
    ):

        best_candidate = None

        best_min_distance = -1

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

            if min_distance > best_min_distance:

                best_min_distance = (
                    min_distance
                )

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


# --------------------------------------------------
# Determine relative area name
# --------------------------------------------------

def get_area_name(
    candidate,
    city_polygon
):

    representative = (
        city_polygon.representative_point()
    )

    center_lat = representative.y
    center_lon = representative.x

    lat_difference = (
        candidate["lat"]
        - center_lat
    )

    lon_difference = (
        candidate["lon"]
        - center_lon
    )

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
        lat_difference
        / lat_range
    )

    lon_ratio = (
        lon_difference
        / lon_range
    )

    # --------------------------------------------------
    # Central area
    # --------------------------------------------------

    if (
        abs(lat_ratio) < 0.15
        and abs(lon_ratio) < 0.15
    ):

        return "Central"

    # --------------------------------------------------
    # Dominant direction
    # --------------------------------------------------

    if abs(lat_ratio) >= abs(lon_ratio):

        if lat_ratio > 0:
            return "North"

        return "South"

    if lon_ratio > 0:
        return "East"

    return "West"


# --------------------------------------------------
# Generate candidates
# --------------------------------------------------

def generate_candidates(city):

    print(
        "\nGetting city boundary for:",
        city
    )

    boundary = get_city_boundary(
        city
    )

    feature = (
        boundary["features"][0]
    )

    geometry = feature["geometry"]

    city_polygon = shape(
        geometry
    )

    if city_polygon.is_empty:

        raise ValueError(
            f"Empty city polygon: {city}"
        )

    # --------------------------------------------------
    # Generate many possible points
    # --------------------------------------------------

    candidate_pool = (
        generate_candidate_pool(
            city_polygon
        )
    )

    print(
        "Candidate pool:",
        len(candidate_pool)
    )

    if not candidate_pool:

        raise ValueError(
            f"No candidate points found "
            f"inside {city} boundary"
        )

    # --------------------------------------------------
    # Select spatially diverse points
    # --------------------------------------------------

    selected = (
        select_diverse_candidates(
            candidate_pool,
            TARGET_CANDIDATES
        )
    )

    if len(selected) < TARGET_CANDIDATES:

        raise ValueError(
            f"Could only generate "
            f"{len(selected)} candidates "
            f"for {city}"
        )

    # --------------------------------------------------
    # Add names
    # --------------------------------------------------

    locations = []

    used_names = set()

    for index, candidate in enumerate(
        selected
    ):

        area_name = get_area_name(
            candidate,
            city_polygon
        )

        # Avoid duplicate area labels.
        if area_name in used_names:

            area_name = (
                f"Area {index + 1}"
            )

        used_names.add(
            area_name
        )

        locations.append(
            {
                "name": (
                    f"{area_name} {city}"
                ),

                "lat": candidate["lat"],

                "lon": candidate["lon"],
            }
        )

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    print(
        "\n===== SPATIALLY DISTRIBUTED CANDIDATES ====="
    )

    for location in locations:

        print(
            location["name"],
            "| LAT:",
            round(
                location["lat"],
                6
            ),
            "| LON:",
            round(
                location["lon"],
                6
            )
        )

    print(
        "Total candidates:",
        len(locations)
    )

    print(
        "=============================================\n"
    )

    return locations


# --------------------------------------------------
# Location Node
# --------------------------------------------------

def location_node(
    state: ResearchState
):

    city = state["city"]

    print(
        "\nGenerating spatial candidates for:",
        city
    )

    locations = generate_candidates(
        city
    )

    return {
        "locations": locations
    }