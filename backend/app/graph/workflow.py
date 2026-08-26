from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.planner import planner_node
from app.agents.location import location_node
from app.agents.scoring import scoring_node
from app.agents.report import report_node

builder = StateGraph(ResearchState)


builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "location",
    location_node
)

builder.add_node(
    "scoring",
    scoring_node
)

builder.add_node(
    "report",
    report_node
)


builder.add_edge(
    START,
    "planner"
)

builder.add_edge(
    "planner",
    "location"
)

builder.add_edge(
    "location",
    "scoring"
)

builder.add_edge(
    "scoring",
    "report"
)

builder.add_edge(
    "report",
    END
)


graph = builder.compile()