from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MatchingInputDTO:
    lead_id: int
    property_id: int
    score: float  # 0–100
    reasons_json: Dict[str, Any]
