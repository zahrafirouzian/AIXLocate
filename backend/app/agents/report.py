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

The scoring system has already selected the recommended location.
Your job is ONLY to explain why this location ranked highest among
the evaluated candidates.

Recommended Location:
{location}

Selected Location Data:
{best_location_data}

All Locations:
{locations}


STRICT RULES:

- Do not change the recommendation.
- Do not suggest alternatives.
- Use only the provided numbers.
- When comparing scores, include the compared values.
- Do not use human-comfort terminology.
- Do not use the words:
  comfort, discomfort, safety, ideal weather, pleasant, unpleasant.
- Do not describe thermal score as thermal comfort.
- Describe thermal score only as a technical infrastructure metric.
- Describe cooling score only as cooling efficiency or estimated cooling performance.
- Treat risk_score only as a numerical infrastructure/environmental score.
- Do not describe risk_score as danger, risk level, or safety.
- Do not invent standards, thresholds, measurements, costs, savings,
  reliability, or other data.
- Do not introduce metrics that are not provided.
- Do not describe the climate as good or bad.
- Use technical data-center infrastructure language only.


IMPORTANT LANGUAGE RULES:

- The recommendation is comparative, not absolute.
- The selected location is the strongest candidate ONLY among the
  evaluated locations.
- Do not claim that it is the objectively best location.
- Do not claim that it is the ideal location.
- Do not use exaggerated language.
- Do not use words such as:
  ideal, perfect, optimal, best possible, guaranteed,
  excellent choice, superior location.
- Do not imply certainty beyond the provided data.
- Do not claim guaranteed energy savings, cost savings, reliability,
  performance improvements, or operational benefits.
- If the score difference between candidates is small, explicitly state
  that the ranking is close.
- Describe advantages as relative advantages compared with the evaluated
  candidates.
- Clearly distinguish between "highest-ranked candidate" and
  "objectively best location".


PREFERRED WORDING:

Use phrases such as:

- "performed best among the evaluated candidates"
- "ranked highest in this analysis"
- "achieved the highest suitability score"
- "showed comparatively stronger cooling performance"
- "showed a higher technical infrastructure score"
- "is the strongest candidate among the evaluated locations"
- "based on the analyzed data"


AVOID:

- "ideal location"
- "perfect location"
- "optimal location"
- "best possible location"
- "guaranteed to perform better"
- "will reduce costs"
- "will save energy"


REPORT FORMAT:

Recommended Location:
<name>


Suitability Score:
<number>/100


Why Selected:
Explain why this location ranked highest among the evaluated candidates.
Use the actual metrics and compare them with relevant competing locations.
If the score difference is small, explicitly mention that the ranking is close.


Key Advantages:
- Compare cooling performance using actual values.
- Compare thermal performance using actual values.
- Mention the suitability score and relevant comparison.


Conclusion:
Write ONE sentence stating that this location is the strongest candidate
among the evaluated locations based on the analyzed climate and
environmental data.

The conclusion must NOT describe the location as ideal, optimal,
perfect, objectively best, or guaranteed to perform better.
"""

    report = ask_llm(prompt)

    return {
        "report": report
    }