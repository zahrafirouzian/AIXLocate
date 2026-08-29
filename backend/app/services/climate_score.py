def calculate_climate_score(stats_data):

    temperature_stats = stats_data.get(
        "temperature_stats",
        {}
    )

    mean_temp = temperature_stats.get(
        "mean"
    )

    if mean_temp is None:
        return 0

    mean_temp = float(mean_temp)

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

    else:
        return 50