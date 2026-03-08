# IAService — versão BALANCEADA + métodos para dashboard

from typing import Dict, Any, List
from src.domain.ia.entities.ia_entity import IAEntity
from src.infrastructure.ia.repositories.ia_repository import IARepository
from src.application.ia.engine.ia_engine import IAEngine


class IAService:

    def __init__(self, ia_repo: IARepository, ia_engine: IAEngine, lead_repo, property_repo):
        self.ia_repo = ia_repo
        self.ia_engine = ia_engine
        self.lead_repo = lead_repo
        self.property_repo = property_repo

    # ---------------------------------------------------------
    # EXECUTAR IA PARA UM LEAD
    # ---------------------------------------------------------
    def run_for_lead(self, lead_id: int) -> Dict[str, Any]:
        lead = self.lead_repo.buscar_por_id(lead_id)
        if not lead:
            raise Exception(f"Lead {lead_id} não encontrado")

        props = self.property_repo.find()
        results = []

        for prop in props:
            (
                similarity,
                conversion_score,
                lead_vector,
                property_vector,
                reasons_json
            ) = self.ia_engine.executar(lead.__dict__, prop)

            # -----------------------------
            # FILTRO BALANCEADO — versão final
            # -----------------------------
            if similarity < 0.05:
                continue

            if conversion_score < 5:
                continue

            entity = IAEntity(
                id=None,
                lead_id=lead.id,
                property_id=prop.id,
                similarity=similarity,
                conversion_score=conversion_score,
                lead_vector=lead_vector,
                property_vector=property_vector,
                reasons_json=reasons_json,
                created_at=IAEntity.now_iso()
            )

            self.ia_repo.save(entity)

            results.append({
                "property_id": prop.id,
                "similarity": similarity,
                "conversion_score": conversion_score,
                "reasons": reasons_json
            })

        avg_conv = round(
            sum(r["conversion_score"] for r in results) / len(results),
            2
        ) if results else 0.0

        return {
            "lead_id": lead.id,
            "results": results,
            "average_conversion": avg_conv,
            "total": len(results)
        }

    # ---------------------------------------------------------
    # EXECUTAR IA PARA TODOS OS LEADS
    # ---------------------------------------------------------
    def run_all(self):
        leads = self.lead_repo.consultar()
        for lead in leads:
            self.run_for_lead(lead.id)

    # ---------------------------------------------------------
    # NOVO: LISTAR TODOS OS SCORES
    # ---------------------------------------------------------
    def get_all_scores(self) -> List[IAEntity]:
        return self.ia_repo.list_all()

    # ---------------------------------------------------------
    # NOVO: AGRUPAR SCORES POR LEAD
    # ---------------------------------------------------------
    def get_grouped_scores(self) -> Dict[int, List[IAEntity]]:
        return self.ia_repo.list_grouped_by_lead()
