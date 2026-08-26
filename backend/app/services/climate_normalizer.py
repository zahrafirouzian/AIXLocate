def normalize_climate_data(location):

    temperature = location["temperature"]

    solar = location["solar_ghi"]


    # Cooling score
    cooling_score = max(
        0,
        100 - (temperature * 1.5)
    )


    # Thermal score
    thermal_score = max(
        0,
        100 - abs(temperature - 25) * 5
    )


    # Solar risk
    risk_score = max(
        0,
        100 - (solar / 20)
    )


    return {

        **location,

        "cooling_score": round(cooling_score,2),

        "thermal_score": round(thermal_score,2),

        "risk_score": round(risk_score,2)

    }
