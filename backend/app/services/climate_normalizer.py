def normalize_climate_data(location):

    temperature = location["temperature"]
    solar = location["solar_ghi"]

    return {
        **location,

        "temperature": round(
            temperature,
            2
        ),

        "solar_ghi": round(
            solar,
            2
        ),

        "solar_dni": round(
            location.get("solar_dni", 0),
            2
        ),

        "climate_score": round(
            location.get("climate_score", 0),
            2
        )
    }