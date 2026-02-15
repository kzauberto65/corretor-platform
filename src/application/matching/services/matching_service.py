import json
from typing import List

from src.domain.matching.entities.matching_entity import MatchingEntity
from src.domain.matching.dto.matching_result_dto import MatchingResultDTO
from src.infrastructure.matching.repositories.matching_repository import MatchingRepository
from src.application.matching.engine.matching_engine import MatchingEngine


class MatchingService:
    def __init__(self, matching_repo: MatchingRepository, matching_engine: MatchingEngine, lead_repo, property_repo):
        self.matching_repo = matching_repo
        self.matching_engine = matching_engine
        self.lead_repo = lead_repo
        self.property_repo = property_repo

    def run_for_lead(self, lead_id: int) -> MatchingResultDTO:
        # ✔ usa o método correto do seu LeadRepository
        lead = self.lead_repo.buscar_por_id(lead_id)

        if not lead:
            raise Exception(f"Lead {lead_id} não encontrado")

        # ✔ usa o método correto do seu EmpreendimentoRepository
        props = self.property_repo.find()

        matches = []

        for prop in props:
            score, reasons = self.matching_engine.match(lead, prop)

            if score < 50:
                continue

            entity = MatchingEntity(
                id=None,
                lead_id=lead.id,
                property_id=prop.id,
                score=score,
                reasons_json=reasons
            )

            self.matching_repo.save(entity)

            matches.append({
                "property_id": prop.id,
                "score": score,
                "reasons": reasons
            })

        avg_score = round(sum(m["score"] for m in matches) / len(matches), 2) if matches else 0.0

        return MatchingResultDTO(
            lead_id=lead.id,
            matches=matches,
            average_score=avg_score,
            total=len(matches)
        )

    def run_all(self):
        # ✔ usa o método correto do seu LeadRepository
        leads = self.lead_repo.consultar()

        for lead in leads:
            self.run_for_lead(lead.id)
