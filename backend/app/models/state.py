from typing import TypedDict, List, Optional


class LocationResult(TypedDict):

    name: str

    lat: float

    lon: float

    temperature: float

    solar_ghi: float

    solar_dni: float

    cooling_score: float

    thermal_score: float

    risk_score: float

    suitability_score: float



class ResearchState(TypedDict):

    query: str

    city: str

    locations: List[LocationResult]

    recommendation: str

    report: str