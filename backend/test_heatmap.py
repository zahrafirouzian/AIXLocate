from app.services.city_boundary import get_city_boundary
from app.services.heatmap_aoi import create_heatmap_aoi
from app.tools.fortyguard_heatmap import create_heatmap


city = "Phoenix, Arizona, USA"


print(f"Getting boundary: {city}")

boundary = get_city_boundary(city)

print(
    "Boundary:",
    boundary["features"][0]["geometry"]["type"]
)


aoi = create_heatmap_aoi(
    boundary,
    size_km=1.5
)

print(
    "Heatmap AOI:",
    aoi["features"][0]["geometry"]["type"]
)


payload = {
    "polygon_aoi": aoi,

    "date_time": {
        "start_date": "2024-07-15",
        "start_time": "14:00",
        "filter_type": 1,
    },

    "granularity": 100,
}


print("Requesting FortyGuard Heatmap...")


result = create_heatmap(
    payload
)


print("Heatmap completed!")


heatmap_result = result.get(
    "result",
    {}
)


print("\n=== HEATMAP RESULT ===")


# -------------------------
# Result keys
# -------------------------

print(
    "\nResult keys:",
    heatmap_result.keys()
)


# -------------------------
# Stats
# -------------------------

stats_data = heatmap_result.get(
    "stats_data",
    {}
)


print(
    "\nStats data:"
)

print(
    stats_data
)


# -------------------------
# Map data
# -------------------------

map_data = heatmap_result.get(
    "map_data",
    {}
)


print(
    "\nMap data type:",
    map_data.get("type")
)


features = map_data.get(
    "features",
    []
)


print(
    "Number of features:",
    len(features)
)


# -------------------------
# First feature
# -------------------------

if features:

    print(
        "\nFirst feature:"
    )

    print(
        features[0]
    )

else:

    print(
        "\nNo map features returned."
    )


# -------------------------
# Activity information
# -------------------------

print(
    "\nActivity ID:",
    result.get("activity_id")
)

print(
    "Status:",
    result.get("status")
)