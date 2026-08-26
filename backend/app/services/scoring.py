def calculate_cooling_score(temperature):

    score = 100 - abs(temperature - 30) * 5

    return max(0, min(score, 100))



def calculate_thermal_score(heat_stress):

    score = 100 - heat_stress

    return max(0, min(score, 100))



def calculate_risk_score():

    return 80



def calculate_suitability(location):

    cooling = calculate_cooling_score(
        location["temperature"]
    )

    thermal = calculate_thermal_score(
        location["heat_stress"]
    )

    risk = calculate_risk_score()


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
        "risk_score": risk,
        "suitability_score": round(total,2)
    }