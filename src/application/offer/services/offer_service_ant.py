from src.domain.offer.dto.offer_input_dto import OfferInputDTO
from src.application.offer.normalizers.offer_normalizer import OfferNormalizer
from src.application.offer.matching.matching_engine import MatchingEngine


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

    def _to_float(self, value, default=0.0):
        """
        Converte valores vindos do banco (string, None, int)
        para float de forma segura.
        """
        try:
            if value is None:
                return default
            return float(value)
        except:
            return default

    def generate_offers_for_lead(self, lead_id: int, score_threshold: float = 0.2):

        lead_entity = self.lead_repository.buscar_por_id(lead_id)
        if not lead_entity:
            print(f"[DEBUG] Lead {lead_id} não encontrado")
            return 0

        # 🔥 Conversão segura
        lead = {
            "id": lead_entity.id,
            "preco_min": self._to_float(lead_entity.preco_min, 0.0),
            "preco_max": self._to_float(lead_entity.preco_max, 999999999.0),
            "bairro_interesse": lead_entity.bairro_interesse,
            "cidade_interesse": lead_entity.cidade_interesse,
            "tipo_imovel": lead_entity.tipo_imovel,
            "intencao": lead_entity.intencao,
            "urgencia": lead_entity.urgencia,
        }

        empreendimentos = self.empreendimento_repository.find()

        # 🔥 DEBUG: quantidade de empreendimentos
        print(f"[DEBUG] Lead {lead['id']} → {len(empreendimentos)} empreendimentos encontrados")

        count = 0
        for e in empreendimentos:

            empreendimento = {
                "id": e.id,
                "preco": self._to_float(e.preco, 0.0),
                "bairro": e.bairro,
                "cidade": e.cidade,
                "regiao": e.regiao,
                "estado": e.estado,
                "tipo": e.tipo,
                "produto": e.produto,
                "tipologia": e.tipologia,
                "status_entrega": e.status_entrega,
                "periodo_lancamento": e.periodo_lancamento,
            }

            score, rationale = self.matching_engine.calculate_score_and_rationale(
                lead,
                empreendimento
            )

            # 🔥 DEBUG DO SCORE
            print(f"[DEBUG] Lead {lead['id']} x Emp {empreendimento['id']} → Score={score} | {rationale}")

            if score >= score_threshold:
                input_dto = OfferInputDTO(
                    lead_id=lead["id"],
                    empreendimento_id=empreendimento["id"],
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

        # 🔥 DEBUG: quantidade de leads
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
    