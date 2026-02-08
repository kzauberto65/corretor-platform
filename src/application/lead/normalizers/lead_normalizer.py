from src.domain.lead.dto.lead_input_dto import LeadInputDTO
from src.domain.lead.dto.lead_normalized_dto import LeadNormalizedDTO


class LeadNormalizer:

    @staticmethod
    def normalize(dto: LeadInputDTO) -> LeadNormalizedDTO:
        def clean(value) -> str | None:
            if value is None:
                return None
            value = str(value).strip()
            return value if value != "" else None

        return LeadNormalizedDTO(
            # Básico
            nome=clean(dto.nome),
            email=clean(dto.email),
            telefone=clean(dto.telefone),
            origem=clean(dto.origem),
            tags=clean(dto.tags),

            # Perfil imobiliário
            intencao=clean(dto.intencao),
            tipo_imovel=clean(dto.tipo_imovel),
            faixa_preco=clean(dto.faixa_preco),
            preco_min=dto.preco_min,
            preco_max=dto.preco_max,
            quartos=dto.quartos,
            vagas=dto.vagas,
            metragem_min=dto.metragem_min,
            metragem_max=dto.metragem_max,
            bairro_interesse=clean(dto.bairro_interesse),
            cidade_interesse=clean(dto.cidade_interesse),
            urgencia=clean(dto.urgencia),
            motivo=clean(dto.motivo),

            # Marketing & Tracking
            utm_source=clean(dto.utm_source),
            utm_medium=clean(dto.utm_medium),
            utm_campaign=clean(dto.utm_campaign),
            utm_term=clean(dto.utm_term),
            utm_content=clean(dto.utm_content),
            canal_preferido=clean(dto.canal_preferido),

            # Dados ricos
            profile_json=dto.dados_completos,
            historico_json=None,

            # Score
            score_lead=None
        )
