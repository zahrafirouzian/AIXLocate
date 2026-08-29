from langgraph.graph import StateGraph, START, END

from app.models.state import ResearchState

from app.agents.planner import planner_node
from app.agents.climate import climate_node
from app.agents.scoring import scoring_node
from app.agents.report import report_node


# ==================================================
# Build Research Workflow
# ==================================================

builder = StateGraph(ResearchState)


# ==================================================
# Nodes
# ==================================================

builder.add_node(
    "planner",
    planner_node
)

builder.add_node(
    "climate",
    climate_node
)

builder.add_node(
    "scoring",
    scoring_node
)

builder.add_node(
    "report",
    report_node
)


# ==================================================
# Workflow
# ==================================================

builder.add_edge(
    START,
    "planner"
)

builder.add_edge(
    "planner",
    "climate"
)

builder.add_edge(
    "climate",
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


# ==================================================
# Compile
# ==================================================

graph = builder.compile()