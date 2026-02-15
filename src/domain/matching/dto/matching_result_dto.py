from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class MatchingResultDTO:
    lead_id: int
    matches: List[Dict[str, Any]]
    average_score: float
    total: int
