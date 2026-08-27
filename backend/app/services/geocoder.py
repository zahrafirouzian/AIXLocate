import requests


def get_city_coordinates(city: str):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": f"{city}, United States",
        "format": "json",
        "limit": 5,
        "addressdetails": 1,
        "countrycodes": "us",
        "featuretype": "city",
    }

    headers = {
        "User-Agent": "AIXLocate/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(
            f"City not found in the United States: {city}"
        )

    city_input = city.strip().lower()

    for result in data:

        address = result.get("address", {})

        country_code = address.get(
            "country_code",
            ""
        ).lower()

        if country_code != "us":
            continue

        result_city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or ""
        ).strip().lower()

        if result_city == city_input:

            return (
                float(result["lat"]),
                float(result["lon"])
            )

    raise ValueError(
        f"'{city}' is not a recognized U.S. city."
    )