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
You are an AI data center analysis report generator.

The scoring system already selected the recommended location.
Your job is ONLY to explain the decision.

Recommended Location:
{location}


Selected Location Data:
{best_location_data}


All Locations:
{locations}


STRICT RULES:

- Do not change the recommendation.
- Do not suggest alternatives.
- Use only provided numbers.
- When comparing scores, always include both values.
- Never describe a score as risk, comfort, or safety unless explicitly provided.
- Risk score: treat it only as a positive score. Do not compare it as risk level.- Do not mention comfort, people, tourism, or weather.
- Do not invent standards or thresholds.
- Do not use words related to human experience such as comfort, discomfort, safety, or ideal weather.
- Do not describe climate as good or bad. Only compare infrastructure performance metrics.
- Use technical infrastructure language only.

Write a short technical report.

Format:

Recommended Location:
<name>


Suitability Score:
<number>/100


Why Selected:
Explain why this location achieved a higher suitability score using the provided metrics.

Key Advantages:
- Compare cooling score
- Compare thermal score
- Mention suitability score


Conclusion:
One sentence recommendation for AI data center deployment.
"""


    report = ask_llm(prompt)

    return {
        "report": report
    }