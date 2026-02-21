# src/domain/ia/entities/ia_entity.py

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class IAEntity:
    """
    Entidade que representa um registro completo da tabela ia_score.
    Segue o mesmo padrão de MatchingEntity, adaptado para IA.
    """

    id: int | None
    lead_id: int
    property_id: int
    similarity: float              # 0–1
    conversion_score: float        # 0–100
    lead_vector: Dict[str, Any]    # vetor numérico serializado
    property_vector: Dict[str, Any]
    reasons_json: Dict[str, Any]
    created_at: str | None = None  # ISO 8601

    @staticmethod
    def now_iso() -> str:
        """Retorna timestamp ISO no mesmo padrão usado no MVP."""
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
