from src.domain.lead.dto.lead_input_dto import LeadInputDTO
from src.domain.lead.dto.lead_dto import LeadDTO
from src.domain.lead.entities.lead_entity import LeadEntity
from src.application.lead.normalizers.lead_normalizer import LeadNormalizer
from src.infrastructure.lead.repositories.lead_repository import LeadRepository


class LeadService:

    def __init__(self, repository: LeadRepository):
        self.repository = repository

    # ---------------------------------------------------------
    # CADASTRAR
    # ---------------------------------------------------------
    def cadastrar(self, dto: LeadInputDTO) -> LeadDTO:
        normalized = LeadNormalizer.normalize(dto)

        entity = LeadEntity(
            id=None,

            # Básico
            nome=normalized.nome,
            email=normalized.email,
            telefone=normalized.telefone,
            origem=normalized.origem,
            tags=normalized.tags,

            # Perfil imobiliário
            intencao=normalized.intencao,
            tipo_imovel=normalized.tipo_imovel,
            faixa_preco=normalized.faixa_preco,
            preco_min=normalized.preco_min,
            preco_max=normalized.preco_max,
            quartos=normalized.quartos,
            vagas=normalized.vagas,
            metragem_min=normalized.metragem_min,
            metragem_max=normalized.metragem_max,
            bairro_interesse=normalized.bairro_interesse,
            cidade_interesse=normalized.cidade_interesse,
            urgencia=normalized.urgencia,
            motivo=normalized.motivo,

            # Marketing & Tracking
            utm_source=normalized.utm_source,
            utm_medium=normalized.utm_medium,
            utm_campaign=normalized.utm_campaign,
            utm_term=normalized.utm_term,
            utm_content=normalized.utm_content,
            canal_preferido=normalized.canal_preferido,

            # Dados ricos
            profile_json=normalized.profile_json,
            historico_json=normalized.historico_json,

            # Score
            score_lead=normalized.score_lead,

            # Auditoria
            criado_em=None,
            atualizado_em=None
        )

        created = self.repository.cadastrar(entity)
        return LeadDTO(**created.__dict__)

    # ---------------------------------------------------------
    # ATUALIZAR
    # ---------------------------------------------------------
    def atualizar(self, id: int, dto: LeadInputDTO) -> LeadDTO:
        normalized = LeadNormalizer.normalize(dto)

        entity = LeadEntity(
            id=id,

            # Básico
            nome=normalized.nome,
            email=normalized.email,
            telefone=normalized.telefone,
            origem=normalized.origem,
            tags=normalized.tags,

            # Perfil imobiliário
            intencao=normalized.intencao,
            tipo_imovel=normalized.tipo_imovel,
            faixa_preco=normalized.faixa_preco,
            preco_min=normalized.preco_min,
            preco_max=normalized.preco_max,
            quartos=normalized.quartos,
            vagas=normalized.vagas,
            metragem_min=normalized.metragem_min,
            metragem_max=normalized.metragem_max,
            bairro_interesse=normalized.bairro_interesse,
            cidade_interesse=normalized.cidade_interesse,
            urgencia=normalized.urgencia,
            motivo=normalized.motivo,

            # Marketing & Tracking
            utm_source=normalized.utm_source,
            utm_medium=normalized.utm_medium,
            utm_campaign=normalized.utm_campaign,
            utm_term=normalized.utm_term,
            utm_content=normalized.utm_content,
            canal_preferido=normalized.canal_preferido,

            # Dados ricos
            profile_json=normalized.profile_json,
            historico_json=normalized.historico_json,

            # Score
            score_lead=normalized.score_lead,

            # Auditoria
            criado_em=None,
            atualizado_em=None
        )

        updated = self.repository.atualizar(entity)
        return LeadDTO(**updated.__dict__)

    # ---------------------------------------------------------
    # CONSULTAR
    # ---------------------------------------------------------
    def consultar(self) -> list[LeadDTO]:
        lista = self.repository.consultar()
        return [LeadDTO(**item.__dict__) for item in lista]

    # ---------------------------------------------------------
    # BUSCAR POR ID
    # ---------------------------------------------------------
    def buscar_por_id(self, id: int) -> LeadDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return LeadDTO(**encontrado.__dict__) if encontrado else None

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
