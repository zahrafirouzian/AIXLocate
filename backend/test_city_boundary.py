from app.services.city_boundary import get_city_boundary


cities = [
    "Phoenix, Arizona, USA",
    "New York, New York, USA",
    "Los Angeles, California, USA",
]


for city in cities:

    print(f"\nFinding boundary: {city}")

    boundary = get_city_boundary(city)

    print(
        "Geometry:",
        boundary["features"][0]["geometry"]["type"]
    )

    print(
        "Features:",
        len(boundary["features"])
    )
