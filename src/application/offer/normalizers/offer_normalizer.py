from src.domain.offer.dto.offer_input_dto import OfferInputDTO
from src.domain.offer.dto.offer_normalized_dto import OfferNormalizedDTO


class OfferNormalizer:
    def normalize(self, dto: OfferInputDTO) -> OfferNormalizedDTO:
        """
        Normaliza os dados da oferta antes de enviar ao Service.
        Não acessa banco, não acessa filesystem.
        Apenas garante tipos e consistência.
        """

        lead_id = int(dto.lead_id)
        empreendimento_id = int(dto.empreendimento_id)
        score = float(dto.score)
        rationale = str(dto.rationale).strip()

        return OfferNormalizedDTO(
            lead_id=lead_id,
            empreendimento_id=empreendimento_id,
            score=score,
            rationale=rationale
        )
