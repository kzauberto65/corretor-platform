# src/domain/ia/dto/ia_input_dto.py

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class IAInputDTO:
    """
    DTO de entrada para o processamento da IA.
    Representa uma combinação lead × imóvel antes de ser persistida.
    """

    lead_id: int
    property_id: int
    similarity: float              # 0–1
    conversion_score: float        # 0–100
    lead_vector: Dict[str, Any]    # vetor numérico serializado
    property_vector: Dict[str, Any]
    reasons_json: Dict[str, Any]
    created_at: str                # ISO 8601
