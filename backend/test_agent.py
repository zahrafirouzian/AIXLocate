from app.graph.workflow import graph


result = graph.invoke(
    {
        "query": "Find best location for 100MW AI data center in Phoenix",
        "city": "",
        "locations": [],
        "recommendation": "",
        "report": ""
    }
)


print(result["report"])
print(result["locations"])