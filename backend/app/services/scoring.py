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


    cooling = calculate_cooling_score(
        temperature
    )


    thermal = calculate_thermal_score(
        temperature
    )


    risk = calculate_risk_score(
        solar
    )


    total = (
        cooling * 0.4
        +
        thermal * 0.4
        +
        risk * 0.2
    )


    return {
        **location,

        "cooling_score": round(cooling,2),

        "thermal_score": round(thermal,2),

        "risk_score": round(risk,2),

        "suitability_score": round(total,2)
    }