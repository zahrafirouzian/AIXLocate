from app.models.state import ResearchState

from app.services.llm import ask_llm


def report_node(state: ResearchState):

    location = state["recommendation"]

    locations = state["locations"]

    best_location_data = next(
loc for loc in locations
if loc["name"] == location
)

    prompt = f"""
You are an AI infrastructure consultant specialized in selecting locations for large-scale AI data centers.

Analyze the recommended location using ONLY the provided climate data.

Recommended Location:
{location}


Recommended Location Data:
{best_location_data}


Alternative Locations:
{locations}

Generate a concise professional recommendation report for AI data center site selection.


The report must focus on:

- Cooling efficiency
- Thermal stress impact on data center operations
- Temperature impact on cooling requirements
- Climate-related infrastructure risks
- Comparison with alternative locations


Important rules:
- Use ONLY the provided data.
- Do not invent climate values.
- Never call a value average, annual, or typical unless explicitly provided.
- Do not describe a location as having a "cool climate" unless supported by comparison data.
- Always compare the recommended location against the alternatives.
- Focus on relative improvement, cooling demand reduction, and infrastructure efficiency.
- Do not exaggerate benefits.

Format:

Recommended Location:
<location>


Suitability Assessment:
<Explain why this location is suitable for an AI data center>


Key Advantages:
- <advantage based on provided data>
- <advantage based on provided data>
- <advantage based on provided data>


Conclusion:
<Final recommendation for AI data center deployment>
"""


    report = ask_llm(prompt)


    return {
        "report": report
    }