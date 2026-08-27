def calculate_cooling_score(temperature):

    score = 100 - abs(temperature - 25) * 4

    return max(0, min(score, 100))


def calculate_thermal_score(temperature):

    score = 100 - abs(temperature - 25) * 3

    return max(0, min(score, 100))


def calculate_risk_score(solar_ghi):

    score = 100 - (solar_ghi / 20)

    return max(0, min(score, 100))


def calculate_suitability(location):

    temperature = location["temperature"]

    solar = location["solar_ghi"]

    climate_score = location.get(
        "climate_score",
        70
    )

    cooling = calculate_cooling_score(
        temperature
    )

    thermal = calculate_thermal_score(
        temperature
    )

    risk = calculate_risk_score(
        solar
    )

    environmental_score = (
        cooling * 0.4
        +
        thermal * 0.4
        +
        risk * 0.2
    )

    final_score = (
        environmental_score * 0.6
        +
        climate_score * 0.4
    )

    return {

        **location,

        "cooling_score": round(
            cooling,
            2
        ),

        "thermal_score": round(
            thermal,
            2
        ),

        "risk_score": round(
            risk,
            2
        ),

        "environmental_score": round(
            environmental_score,
            2
        ),

        "suitability_score": round(
            final_score,
            2
        )
    }