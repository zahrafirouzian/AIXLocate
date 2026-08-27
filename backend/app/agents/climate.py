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


def climate_node(state):

    locations = state["locations"]

    city = state["city"]

    climate_results = []

    # --------------------------------------------------
    # 1. Environment analysis for each candidate
    # --------------------------------------------------

    for location in locations:

        print(
            "Requesting FortyGuard:",
            location["name"]
        )

        data = get_environmental_data(
            lat=location["lat"],
            lon=location["lon"],
            temperature=location.get(
                "temperature",
                25
            )
        )

        print(
            "FortyGuard completed:",
            location["name"]
        )

        result = data["result"]["locations"][0]

        normalized = normalize_climate_data(
            {
                "name": location["name"],
                "lat": location["lat"],
                "lon": location["lon"],
                "temperature": result["temperature"],
                "solar_ghi": result[
                    "solar_irradiance"
                ]["clear_sky"]["ghi"],
                "solar_dni": result[
                    "solar_irradiance"
                ]["clear_sky"]["dni"],
            }
        )

        climate_results.append(
            normalized
        )

    # --------------------------------------------------
    # 2. Create dynamic city boundary
    # --------------------------------------------------

    print(
        "Getting city boundary:",
        city
    )

    boundary = get_city_boundary(city)

    # --------------------------------------------------
    # 3. Create Heatmap AOI
    # --------------------------------------------------

    print(
        "Creating Heatmap AOI:",
        city
    )

    aoi = create_heatmap_aoi(
        boundary,
        size_km=1.5
    )

    # --------------------------------------------------
    # 4. Create FortyGuard Heatmap
    # --------------------------------------------------

    print(
        "Requesting FortyGuard Heatmap:",
        city
    )

    heatmap_result = create_heatmap(
        {
            "polygon_aoi": aoi,

            "date_time": {
                "start_date": "2024-07-15",
                "start_time": "14:00",
                "filter_type": 1,
            },

            "granularity": 100,
        }
    )

    print(
        "FortyGuard Heatmap completed:",
        city
    )

    # --------------------------------------------------
    # 5. Extract Heatmap data
    # --------------------------------------------------

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

    print(
        "Heatmap features:",
        len(
            map_data.get(
                "features",
                []
            )
        )
    )

    # --------------------------------------------------
    # 6. Calculate Climate Score
    # --------------------------------------------------

    climate_score = calculate_climate_score(
        stats_data
    )

    print(
        "Climate Score:",
        climate_score
    )

    for location in climate_results:

        location["climate_score"] = (
            climate_score
        )

    # --------------------------------------------------
    # 7. Return updated State
    # --------------------------------------------------

    return {

        "locations": climate_results,

        "heatmap": map_data,

        "heatmap_stats": stats_data,

    }