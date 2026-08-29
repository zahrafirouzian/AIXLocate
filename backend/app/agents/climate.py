from math import cos, radians

from app.tools.fortyguard_environment import (
    get_environmental_data
)

from app.services.climate_normalizer import (
    normalize_climate_data
)

from app.services.city_boundary import (
    get_city_boundary
)

from app.services.heatmap_aoi import (
    create_heatmap_aoi
)

from app.tools.fortyguard_heatmap import (
    create_heatmap
)

from app.services.climate_score import (
    calculate_climate_score
)


# ==================================================
# FortyGuard analysis configuration
# ==================================================

ANALYSIS_DATE = "2024-07-15"
ANALYSIS_TIME = "14:00"


# ==================================================
# Extract temperature from Heatmap feature
# ==================================================

def extract_feature_temperature(feature):

    properties = feature.get(
        "properties",
        {}
    )

    possible_keys = [
        "average_temperature",
        "temperature",
        "temp",
        "temperature_celsius",
        "temp_celsius",
        "tcm",
    ]

    for key in possible_keys:

        value = properties.get(key)

        if isinstance(
            value,
            (int, float)
        ):

            return float(value)

        if (
            isinstance(value, list)
            and value
        ):

            first_value = value[0]

            if isinstance(
                first_value,
                (int, float)
            ):

                return float(first_value)

    return None


# ==================================================
# Extract all coordinate pairs
# ==================================================

def collect_geometry_points(
    coordinates
):

    points = []

    def collect(value):

        # GeoJSON coordinate:
        # [longitude, latitude]
        if (
            isinstance(
                value,
                (list, tuple)
            )
            and len(value) == 2
            and all(
                isinstance(
                    x,
                    (int, float)
                )
                for x in value
            )
        ):

            points.append(
                (
                    float(value[0]),
                    float(value[1])
                )
            )

            return

        if isinstance(
            value,
            (list, tuple)
        ):

            for item in value:

                collect(item)

    collect(coordinates)

    return points


# ==================================================
# Get approximate Heatmap feature center
# ==================================================

def get_feature_center(
    feature
):

    geometry = feature.get(
        "geometry",
        {}
    )

    coordinates = geometry.get(
        "coordinates"
    )

    if not coordinates:
        return None

    points = collect_geometry_points(
        coordinates
    )

    if not points:
        return None

    avg_lon = (
        sum(
            point[0]
            for point in points
        )
        / len(points)
    )

    avg_lat = (
        sum(
            point[1]
            for point in points
        )
        / len(points)
    )

    return (
        avg_lat,
        avg_lon
    )


# ==================================================
# Geographic distance in meters
# ==================================================

def geographic_distance_meters(
    lat1,
    lon1,
    lat2,
    lon2
):

    meters_per_degree_lat = 111_000

    meters_per_degree_lon = (
        111_000
        * cos(
            radians(
                (lat1 + lat2) / 2
            )
        )
    )

    delta_lat = (
        lat1 - lat2
    )

    delta_lon = (
        lon1 - lon2
    )

    north_south = (
        delta_lat
        * meters_per_degree_lat
    )

    east_west = (
        delta_lon
        * meters_per_degree_lon
    )

    return (
        north_south ** 2
        +
        east_west ** 2
    ) ** 0.5


# ==================================================
# Find nearest Heatmap temperature
# ==================================================

def find_nearest_temperature(
    location,
    features
):

    best_temperature = None

    best_distance = float(
        "inf"
    )

    best_center = None

    for feature in features:

        temperature = (
            extract_feature_temperature(
                feature
            )
        )

        if temperature is None:
            continue

        center = get_feature_center(
            feature
        )

        if center is None:
            continue

        feature_lat, feature_lon = (
            center
        )

        distance = (
            geographic_distance_meters(
                location["lat"],
                location["lon"],
                feature_lat,
                feature_lon
            )
        )

        if distance < best_distance:

            best_distance = distance

            best_temperature = (
                temperature
            )

            best_center = center

    # ==================================================
    # Debug spatial matching
    # ==================================================

    if best_temperature is not None:

        print(
            "\n===== HEATMAP SPATIAL MATCH ====="
        )

        print(
            "Candidate:",
            location["name"]
        )

        print(
            "Candidate coordinates:",
            round(
                location["lat"],
                6
            ),
            round(
                location["lon"],
                6
            )
        )

        print(
            "Matched Heatmap cell:",
            round(
                best_center[0],
                6
            ),
            round(
                best_center[1],
                6
            )
        )

        print(
            "Distance:",
            round(
                best_distance,
                2
            ),
            "meters"
        )

        print(
            "Temperature:",
            best_temperature
        )

        print(
            "=================================\n"
        )

    return best_temperature


# ==================================================
# Climate Node
# ==================================================

def climate_node(
    state
):

    locations = state["locations"]

    city = state["city"]

    climate_results = []

    # ==================================================
    # 1. Get city boundary
    # ==================================================

    print(
        "\nGetting city boundary:",
        city
    )

    boundary = get_city_boundary(
        city
    )

    # ==================================================
    # 2. Create Heatmap AOI
    # ==================================================

    print(
        "\nCreating Heatmap AOI:",
        city
    )

    aoi = create_heatmap_aoi(
        boundary,
        padding_km=0.5
    )

    # ==================================================
    # 3. Request FortyGuard Heatmap
    # ==================================================

    print(
        "\nRequesting FortyGuard Heatmap:",
        city
    )

    heatmap_result = create_heatmap(
        {
            "polygon_aoi": aoi,

            "date_time": {
                "start_date": ANALYSIS_DATE,
                "start_time": ANALYSIS_TIME,
                "filter_type": 1,
            },

            "granularity": 100,

            "analytic_type": "tcm",
        }
    )

    print(
        "\nFortyGuard Heatmap completed:",
        city
    )

    # ==================================================
    # 4. Extract Heatmap data
    # ==================================================

    result_data = heatmap_result.get(
        "result",
        {}
    )

    map_data = result_data.get(
        "map_data",
        {}
    )

    stats_data = result_data.get(
        "stats_data",
        {}
    )

    features = map_data.get(
        "features",
        []
    )

    print(
        "\nHeatmap features:",
        len(features)
    )

    # ==================================================
    # Debug Heatmap statistics
    # ==================================================

    print(
        "\n===== HEATMAP STATS DATA ====="
    )

    print(
        stats_data
    )

    print(
        "================================\n"
    )

    # ==================================================
    # 5. Extract city temperature statistics
    # ==================================================

    temperature_stats = (
        stats_data.get(
            "temperature_stats",
            {}
        )
    )

    mean_temperature = (
        temperature_stats.get(
            "mean"
        )
    )

    minimum_temperature = (
        temperature_stats.get(
            "minimum"
        )
    )

    maximum_temperature = (
        temperature_stats.get(
            "maximum"
        )
    )

    print(
        "\n===== CITY TEMPERATURE STATS ====="
    )

    print(
        "Minimum:",
        minimum_temperature
    )

    print(
        "Mean:",
        mean_temperature
    )

    print(
        "Maximum:",
        maximum_temperature
    )

    print(
        "==================================\n"
    )

    # ==================================================
    # 6. Calculate city-level climate score
    # ==================================================

    climate_score = calculate_climate_score(
        stats_data
    )

    print(
        "Climate Score:",
        climate_score
    )

    # ==================================================
    # 7. Analyze every candidate
    # ==================================================

    for location in locations:

        print(
            "\n======================================"
        )

        print(
            "Analyzing:",
            location["name"]
        )

        print(
            "Coordinates:",
            location["lat"],
            location["lon"]
        )

        print(
            "======================================"
        )

        # ==================================================
        # Candidate -> nearest Heatmap cell
        # ==================================================

        heatmap_temperature = (
            find_nearest_temperature(
                location,
                features
            )
        )

        # ==================================================
        # Fallback to city mean
        # ==================================================

        if heatmap_temperature is None:

            if mean_temperature is None:

                raise ValueError(
                    "Heatmap temperature data "
                    "is unavailable for "
                    f"{location['name']}"
                )

            heatmap_temperature = float(
                mean_temperature
            )

            print(
                "WARNING: No Heatmap cell matched."
            )

            print(
                "Using city mean:",
                heatmap_temperature
            )

        # ==================================================
        # FortyGuard Environment API
        # ==================================================

        print(
            "Requesting FortyGuard environment:"
        )

        data = get_environmental_data(
            lat=location["lat"],
            lon=location["lon"],
            temperature=heatmap_temperature
        )

        print(
            "FortyGuard completed:",
            location["name"]
        )

        # ==================================================
        # Parse Environment result
        # ==================================================

        try:

            result = (
                data["result"]
                ["locations"][0]
            )

        except (
            KeyError,
            IndexError,
            TypeError
        ) as exc:

            raise ValueError(
                "Invalid FortyGuard environment "
                f"response for {location['name']}: "
                f"{data}"
            ) from exc

        # ==================================================
        # Solar data
        # ==================================================

        solar_irradiance = (
            result.get(
                "solar_irradiance",
                {}
            )
        )

        clear_sky = (
            solar_irradiance.get(
                "clear_sky",
                {}
            )
        )

        solar_ghi = clear_sky.get(
            "ghi",
            0
        )

        solar_dni = clear_sky.get(
            "dni",
            0
        )

        # ==================================================
        # Actual local temperature
        # ==================================================

        actual_temperature = float(
            heatmap_temperature
        )

        # ==================================================
        # Debug parsed result
        # ==================================================

        print(
            "\n===== PARSED FORTYGUARD RESULT ====="
        )

        print(
            "NAME:",
            location["name"]
        )

        print(
            "LAT:",
            location["lat"]
        )

        print(
            "LON:",
            location["lon"]
        )

        print(
            "HEATMAP TEMPERATURE:",
            actual_temperature
        )

        print(
            "ENVIRONMENT TEMPERATURE:",
            result.get(
                "temperature"
            )
        )

        print(
            "SOLAR GHI:",
            solar_ghi
        )

        print(
            "SOLAR DNI:",
            solar_dni
        )

        print(
            "=====================================\n"
        )

        # ==================================================
        # Normalize
        # ==================================================

        normalized = (
            normalize_climate_data(
                {
                    "name": location["name"],

                    "lat": location["lat"],

                    "lon": location["lon"],

                    "temperature": (
                        actual_temperature
                    ),

                    "solar_ghi": solar_ghi,

                    "solar_dni": solar_dni,

                    "climate_score": (
                        climate_score
                    ),
                }
            )
        )

        print(
            "\n===== NORMALIZED RESULT ====="
        )

        print(
            normalized
        )

        print(
            "=============================\n"
        )

        climate_results.append(
            normalized
        )

    # ==================================================
    # 8. Return updated state
    # ==================================================

    return {

        "locations": climate_results,

        "heatmap": map_data,

        "heatmap_stats": stats_data,

        "analyzed_locations": len(
            climate_results
        ),

        "analysis_metadata": {

            "city": city,

            "analysis_date": (
                ANALYSIS_DATE
            ),

            "analysis_time": (
                ANALYSIS_TIME
            ),

            "heatmap_features": len(
                features
            ),

            "analyzed_locations": len(
                climate_results
            ),

            "temperature_range": {

                "minimum": (
                    minimum_temperature
                ),

                "mean": (
                    mean_temperature
                ),

                "maximum": (
                    maximum_temperature
                ),
            },
        },
    }