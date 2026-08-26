from app.models.state import ResearchState

def report_node(state: ResearchState):

    location = state["recommendation"]

    report = f"""
Recommended Location:

{location}

Reason:
Best climate conditions for AI data center cooling.
"""

    return {
        "report": report
    }