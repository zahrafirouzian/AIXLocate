from math import sqrt

from shapely.geometry import (
    shape,
    Point
)

from app.models.state import ResearchState

from app.services.city_boundary import (
    get_city_boundary
)


# ==================================================
# Candidate configuration
# ==================================================

TARGET_CANDIDATES = 5

# Dense grid used to generate possible locations.
# A larger grid gives the diversity algorithm
# more choices when selecting spatially separated
# candidates.
GRID_SIZE = 15


# ==================================================
# Geographic distance
# ==================================================

def geographic_distance(
    point_a,
    point_b
):
    """
    Approximate geographic distance between two
    latitude/longitude points.

    Since all candidates belong to the same city,
    this relative distance is sufficient for
    spatial diversification.
    """

    lat1, lon1 = point_a
    lat2, lon2 = point_b

    return sqrt(
        (lat1 - lat2) ** 2
        +
        (lon1 - lon2) ** 2
    )


# ==================================================
# Generate candidate grid inside city boundary
# ==================================================

def generate_candidate_pool(
    city_polygon
):
    """
    Generate a dense grid of possible candidate
    locations and keep only points inside the
    actual city boundary.
    """

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

            # Only keep points that are actually
            # covered by the city polygon.
            if city_polygon.covers(point):

                candidates.append(
                    {
                        "lat": lat,
                        "lon": lon
                    }
                )

    return candidates


# ==================================================
# Select spatially diverse candidates
# ==================================================

def select_diverse_candidates(
    candidates,
    city_polygon,
    target_count=TARGET_CANDIDATES
):
    """
    Select geographically separated candidates.

    Strategy:

    1. Start near the representative point of
       the city polygon.
    2. Repeatedly select the candidate whose
       minimum distance from all selected points
       is largest.

    This creates a spatially diverse set instead
    of simply selecting adjacent grid points.
    """

    if not candidates:

        return []

    # --------------------------------------------------
    # Find a reliable point inside the city.
    # --------------------------------------------------

    representative = (
        city_polygon.representative_point()
    )

    city_center = (
        representative.y,
        representative.x
    )

    # --------------------------------------------------
    # First candidate:
    # closest available grid point to the
    # representative point.
    # --------------------------------------------------

    first_candidate = min(
        candidates,
        key=lambda candidate:
            geographic_distance(
                (
                    candidate["lat"],
                    candidate["lon"]
                ),
                city_center
            )
    )

    selected = [
        first_candidate
    ]

    remaining = [
        candidate
        for candidate in candidates
        if candidate != first_candidate
    ]

    # --------------------------------------------------
    # Greedy max-min diversification.
    # --------------------------------------------------

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

            # Distance to the nearest already
            # selected candidate.
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

            if (
                min_distance
                >
                best_min_distance
            ):

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


# ==================================================
# Determine relative area name
# ==================================================

def get_area_name(
    candidate,
    city_polygon
):
    """
    Give each candidate a human-readable relative
    geographic name such as North, South, East,
    West or Central.

    The name is descriptive only and does not
    affect scoring.
    """

    representative = (
        city_polygon.representative_point()
    )

    center_lat = representative.y
    center_lon = representative.x

    lat_difference = (
        candidate["lat"]
        -
        center_lat
    )

    lon_difference = (
        candidate["lon"]
        -
        center_lon
    )

    lat_range = max(
        city_polygon.bounds[3]
        -
        city_polygon.bounds[1],
        0.000001
    )

    lon_range = max(
        city_polygon.bounds[2]
        -
        city_polygon.bounds[0],
        0.000001
    )

    lat_ratio = (
        lat_difference
        /
        lat_range
    )

    lon_ratio = (
        lon_difference
        /
        lon_range
    )

    # --------------------------------------------------
    # Central area
    # --------------------------------------------------

    if (
        abs(lat_ratio) < 0.18
        and
        abs(lon_ratio) < 0.18
    ):

        return "Central"

    # --------------------------------------------------
    # Dominant direction
    # --------------------------------------------------

    if (
        abs(lat_ratio)
        >=
        abs(lon_ratio)
    ):

        if lat_ratio > 0:

            return "North"

        return "South"

    if lon_ratio > 0:

        return "East"

    return "West"


# ==================================================
# Generate candidates
# ==================================================

def generate_candidates(
    city
):
    """
    Generate five geographically diverse candidate
    locations inside the actual city boundary.
    """

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

    print(
        "Getting city boundary for:",
        city
    )

    boundary = get_city_boundary(
        city
    )

    feature = (
        boundary["features"][0]
    )

    geometry = (
        feature["geometry"]
    )

    city_polygon = shape(
        geometry
    )

    if city_polygon.is_empty:

        raise ValueError(
            f"Empty city polygon: {city}"
        )

    # --------------------------------------------------
    # Generate dense candidate pool
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
    # Select spatially diverse locations
    # --------------------------------------------------

    selected = (
        select_diverse_candidates(
            candidates=candidate_pool,
            city_polygon=city_polygon,
            target_count=TARGET_CANDIDATES
        )
    )

    if (
        len(selected)
        <
        TARGET_CANDIDATES
    ):

        raise ValueError(
            f"Could only generate "
            f"{len(selected)} candidates "
            f"for {city}"
        )

    # --------------------------------------------------
    # Create named locations
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

        # Prevent duplicate directional labels.
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
    # Debug output
    # --------------------------------------------------

    print(
        "\n===== SELECTED SPATIAL CANDIDATES ====="
    )

    for location in locations:

        print(
            f"{location['name']} | "
            f"LAT: {location['lat']} | "
            f"LON: {location['lon']}"
        )

    print(
        "Total candidates:",
        len(locations)
    )

    print(
        "========================================\n"
    )

    return locations


# ==================================================
# Location Node
# ==================================================

def location_node(
    state: ResearchState
):
    """
    Location node.

    Candidate generation is handled by the same
    spatial candidate generator used by the API.
    """

    locations = state.get(
        "locations",
        []
    )

    print(
        "\n===== LOCATION NODE ====="
    )

    print(
        "Candidates received:",
        len(locations)
    )

    for location in locations:

        print(
            f"{location['name']} | "
            f"LAT: {location['lat']} | "
            f"LON: {location['lon']}"
        )

    print(
        "=========================\n"
    )

    return {
        "locations": locations
    }