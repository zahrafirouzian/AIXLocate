from app.graph.workflow import graph


result = graph.invoke(
    {
        "query": "Find the best location for a 100MW AI data center in Phoenix",

        "locations": [
            {
                "name": "North Phoenix",
                "lat": 33.7,
                "lon": -112.1,
                "temperature": 38,
                "heat_stress": 65
            },
            {
                "name": "Downtown Phoenix",
                "lat": 33.44,
                "lon": -112.07,
                "temperature": 44,
                "heat_stress": 85
            }
        ],

        "recommendation": None,
        "report": None
    }
)


print(result["report"])

print("\n--- SCORES ---")

print(result["locations"])