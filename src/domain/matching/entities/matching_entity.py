from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class MatchingEntity:
    id: int | None
    lead_id: int
    property_id: int
    score: float  # 0–100
    reasons_json: Dict[str, Any]
    created_at: str | None = None

    @staticmethod
    def now_iso() -> str:
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
