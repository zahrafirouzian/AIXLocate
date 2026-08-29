def calculate_cooling_score(temperature):

    ideal_temperature = 22.0

    distance = abs(
        temperature - ideal_temperature
    )

    score = 100 - (
        distance * 4
    )

    return max(
        0,
        min(score, 100)
    )


def calculate_thermal_score(temperature):

    ideal_temperature = 22.0

    distance = abs(
        temperature - ideal_temperature
    )

    score = 100 - (
        distance * 3
    )

    return max(
        0,
        min(score, 100)
    )


def calculate_risk_score(solar_ghi):

    # Higher irradiance means higher potential
    # thermal/solar load on infrastructure.

    score = 100 - (
        solar_ghi / 20
    )

    return max(
        0,
        min(score, 100)
    )


def calculate_suitability(location):

    temperature = float(
        location["temperature"]
    )

    solar = float(
        location["solar_ghi"]
    )

    climate_score = float(
        location.get(
            "climate_score",
            0
        )
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

    # --------------------------------------------------
    # Environmental performance
    # --------------------------------------------------

    environmental_score = (
        cooling * 0.35
        +
        thermal * 0.35
        +
        risk * 0.30
    )

    # --------------------------------------------------
    # Final suitability
    # --------------------------------------------------

    final_score = (
        environmental_score * 0.60
        +
        climate_score * 0.40
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