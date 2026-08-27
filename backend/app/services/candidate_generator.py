def generate_candidates(city: str):

    city = city.lower().strip()

    if city == "phoenix":

        return [
            {
                "name": "North Phoenix",
                "lat": 33.70,
                "lon": -112.10,
                "temperature": 38,
                "heat_stress": 65,
            },
            {
                "name": "Downtown Phoenix",
                "lat": 33.44,
                "lon": -112.07,
                "temperature": 44,
                "heat_stress": 85,
            },
        ]

    return [
        {
            "name": city.title(),
            "lat": 33.70,
            "lon": -112.10,
            "temperature": 35,
            "heat_stress": 60,
        }
    ]
