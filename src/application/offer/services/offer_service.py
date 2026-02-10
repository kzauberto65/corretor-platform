from src.domain.offer.dto.offer_input_dto import OfferInputDTO
from src.application.offer.normalizers.offer_normalizer import OfferNormalizer
from src.application.offer.matching.matching_engine import MatchingEngine

from src.application.lead.normalizers.lead_normalizer import LeadNormalizer
from src.application.empreendimento.normalizers.empreendimento_normalizer import EmpreendimentoNormalizer


class OfferService:
    def __init__(
        self,
        offer_repository,
        lead_repository,
        empreendimento_repository
    ):
        self.offer_repository = offer_repository
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

        self.normalizer = OfferNormalizer()
        self.matching_engine = MatchingEngine()

    def generate_offers_for_lead(self, lead_id: int, score_threshold: float = 0.2):

        lead_entity = self.lead_repository.buscar_por_id(lead_id)
        if not lead_entity:
            print(f"[DEBUG] Lead {lead_id} não encontrado")
            return 0

        # Lead normalizado → dict
        lead = LeadNormalizer.normalize(lead_entity)

        empreendimentos = self.empreendimento_repository.find()

        print(f"[DEBUG] Lead {lead['id']} → {len(empreendimentos)} empreendimentos encontrados")

        count = 0
        for e in empreendimentos:

            # Empreendimento normalizado → DTO/objeto
            empreendimento = EmpreendimentoNormalizer.normalize(e)

            # MatchingEngine aceita dict (lead) e objeto (empreendimento)
            score, rationale = self.matching_engine.calculate_score_and_rationale(
                lead,
                empreendimento
            )

            print(
                f"[DEBUG] Lead {lead['id']} x Emp {empreendimento.id} "
                f"→ Score={score} | {rationale}"
            )

            if score >= score_threshold:
                input_dto = OfferInputDTO(
                    lead_id=lead["id"],
                    empreendimento_id=empreendimento.id,
                    score=score,
                    rationale=rationale
                )

                normalized_dto = self.normalizer.normalize(input_dto)
                self.offer_repository.save(normalized_dto)
                count += 1

        print(f"[DEBUG] Total de ofertas salvas para lead {lead['id']}: {count}")
        return count

    def generate_offers_for_all_leads(self, score_threshold: float = 0.2):

        leads = self.lead_repository.consultar()

        print(f"[DEBUG] Qtd de leads encontrados: {len(leads)}")

        total = 0

        for lead in leads:
            print(f"[DEBUG] Gerando ofertas para lead {lead.id}")
            total += self.generate_offers_for_lead(
                lead.id,
                score_threshold=score_threshold
            )

        print(f"[DEBUG] Total geral de ofertas geradas: {total}")
        return total
