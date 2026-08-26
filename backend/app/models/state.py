from typing import TypedDict, List


class LocationResult(TypedDict):
    name: str
    score: float
    reason: str


class ResearchState(TypedDict):
    query: str
    city: str
    locations: List[LocationResult]
    recommendation: str
    report: str
