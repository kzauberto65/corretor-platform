from src.domain.mailing.dto.mailing_input_dto import MailingInputDTO
from src.domain.mailing.dto.mailing_dto import MailingDTO
from src.domain.mailing.entities.mailing_entity import MailingEntity
from src.application.mailing.normalizers.mailing_normalizer import MailingNormalizer
from src.infrastructure.mailing.repositories.mailing_repository import MailingRepository


class MailingService:

    def __init__(self, repository: MailingRepository):
        self.repository = repository

    def cadastrar(self, dto: MailingInputDTO) -> MailingDTO:
        normalized = MailingNormalizer.normalize(dto)

        entity = MailingEntity(
            id=None,

            # Básico
            nome=normalized.nome,
            email=normalized.email,
            telefone=normalized.telefone,
            origem=normalized.origem,
            tags=normalized.tags,

            # Datas e ingestão
            data_ingestao=normalized.data_ingestao,
            fonte_arquivo=normalized.fonte_arquivo,

            # Validação
            valido=normalized.valido,
            motivo_invalidacao=normalized.motivo_invalidacao,
            hash_unico=normalized.hash_unico,

            # Perfil pessoal
            sexo=normalized.sexo,
            data_nascimento=normalized.data_nascimento,
            idade=normalized.idade,
            estado_civil=normalized.estado_civil,
            nacionalidade=normalized.nacionalidade,
            profissao=normalized.profissao,
            empresa=normalized.empresa,
            cargo=normalized.cargo,
            renda_mensal=normalized.renda_mensal,
            faixa_renda=normalized.faixa_renda,
            escolaridade=normalized.escolaridade,

            # Endereço
            cep=normalized.cep,
            logradouro=normalized.logradouro,
            numero=normalized.numero,
            complemento=normalized.complemento,
            bairro=normalized.bairro,
            cidade=normalized.cidade,
            estado=normalized.estado,
            pais=normalized.pais,

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
            primeiro_contato=normalized.primeiro_contato,
            ultimo_contato=normalized.ultimo_contato,
            canal_preferido=normalized.canal_preferido,
            score_mailing=normalized.score_mailing,

            # Auditoria
            criado_em=None,
            atualizado_em=None
        )

        created = self.repository.cadastrar(entity)
        return MailingDTO(**created.__dict__)

    def atualizar(self, id: int, dto: MailingInputDTO) -> MailingDTO:
        normalized = MailingNormalizer.normalize(dto)

        entity = MailingEntity(
            id=id,

            # Básico
            nome=normalized.nome,
            email=normalized.email,
            telefone=normalized.telefone,
            origem=normalized.origem,
            tags=normalized.tags,

            # Datas e ingestão
            data_ingestao=normalized.data_ingestao,
            fonte_arquivo=normalized.fonte_arquivo,

            # Validação
            valido=normalized.valido,
            motivo_invalidacao=normalized.motivo_invalidacao,
            hash_unico=normalized.hash_unico,

            # Perfil pessoal
            sexo=normalized.sexo,
            data_nascimento=normalized.data_nascimento,
            idade=normalized.idade,
            estado_civil=normalized.estado_civil,
            nacionalidade=normalized.nacionalidade,
            profissao=normalized.profissao,
            empresa=normalized.empresa,
            cargo=normalized.cargo,
            renda_mensal=normalized.renda_mensal,
            faixa_renda=normalized.faixa_renda,
            escolaridade=normalized.escolaridade,

            # Endereço
            cep=normalized.cep,
            logradouro=normalized.logradouro,
            numero=normalized.numero,
            complemento=normalized.complemento,
            bairro=normalized.bairro,
            cidade=normalized.cidade,
            estado=normalized.estado,
            pais=normalized.pais,

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
            primeiro_contato=normalized.primeiro_contato,
            ultimo_contato=normalized.ultimo_contato,
            canal_preferido=normalized.canal_preferido,
            score_mailing=normalized.score_mailing,

            # Auditoria
            criado_em=None,
            atualizado_em=None
        )

        updated = self.repository.atualizar(entity)
        return MailingDTO(**updated.__dict__)

    def consultar(self) -> list[MailingDTO]:
        lista = self.repository.consultar()
        return [MailingDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> MailingDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return MailingDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
