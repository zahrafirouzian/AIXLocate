# ============================================================
# Data Center Climate & Environmental Scoring
# ============================================================


# ------------------------------------------------------------
# Cooling Efficiency Score
# ------------------------------------------------------------
# Lower outdoor temperature generally reduces cooling demand.
#
# The score is intentionally gradual:
# - <= 22°C  -> excellent
# - 30°C     -> still relatively strong
# - 40°C     -> significantly reduced
# - >= 45°C  -> very low
# ------------------------------------------------------------

def calculate_cooling_score(temperature):

    temperature = float(temperature)

    if temperature <= 22:
        score = 100

    elif temperature <= 30:
        score = 100 - (
            (temperature - 22) * 3
        )

    elif temperature <= 35:
        score = 76 - (
            (temperature - 30) * 4
        )

    elif temperature <= 40:
        score = 56 - (
            (temperature - 35) * 5
        )

    else:
        score = 31 - (
            (temperature - 40) * 6
        )

    return max(
        0,
        min(score, 100)
    )


# ------------------------------------------------------------
# Thermal Infrastructure Score
# ------------------------------------------------------------
# Represents the relative thermal suitability of the
# environment for infrastructure.
#
# This is NOT human thermal comfort.
# ------------------------------------------------------------

def calculate_thermal_score(temperature):

    temperature = float(temperature)

    if temperature <= 22:
        score = 100

    elif temperature <= 30:
        score = 100 - (
            (temperature - 22) * 2.5
        )

    elif temperature <= 35:
        score = 80 - (
            (temperature - 30) * 3
        )

    elif temperature <= 40:
        score = 65 - (
            (temperature - 35) * 4
        )

    else:
        score = 45 - (
            (temperature - 40) * 5
        )

    return max(
        0,
        min(score, 100)
    )


# ------------------------------------------------------------
# Solar / Environmental Load Score
# ------------------------------------------------------------
# Higher GHI can indicate greater solar loading on the
# infrastructure.
#
# This is treated as a relative numerical environmental
# metric, not a safety metric.
# ------------------------------------------------------------

def calculate_risk_score(solar_ghi):

    solar_ghi = float(solar_ghi)

    score = 100 - (
        solar_ghi / 20
    )

    return max(
        0,
        min(score, 100)
    )


# ------------------------------------------------------------
# Final Data Center Suitability Score
# ------------------------------------------------------------

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

    # --------------------------------------------------------
    # Individual metrics
    # --------------------------------------------------------

    cooling = calculate_cooling_score(
        temperature
    )

    thermal = calculate_thermal_score(
        temperature
    )

    risk = calculate_risk_score(
        solar
    )

    # --------------------------------------------------------
    # Environmental performance
    #
    # Cooling efficiency:
    # 35%
    #
    # Thermal infrastructure:
    # 35%
    #
    # Solar/environmental load:
    # 30%
    # --------------------------------------------------------

    environmental_score = (
        cooling * 0.35
        +
        thermal * 0.35
        +
        risk * 0.30
    )

    # --------------------------------------------------------
    # Final suitability
    #
    # Environmental performance: 60%
    # City-level climate score: 40%
    # --------------------------------------------------------

    final_score = (
        environmental_score * 0.60
        +
        climate_score * 0.40
    )

    # --------------------------------------------------------
    # Return original location data + scoring metrics
    # --------------------------------------------------------

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