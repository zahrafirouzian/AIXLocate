def calculate_climate_score(stats_data):

    mean_temp = stats_data.get(
        "mean",
        40
    )

    if mean_temp <= 30:
        return 100

    elif mean_temp <= 35:
        return 90

    elif mean_temp <= 38:
        return 80

    elif mean_temp <= 40:
        return 70

    elif mean_temp <= 42:
        return 60

    return 50