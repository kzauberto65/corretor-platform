from src.domain.mailing.dto.mailing_input_dto import MailingInputDTO
from src.domain.mailing.dto.mailing_normalized_dto import MailingNormalizedDTO


class MailingNormalizer:

    @staticmethod
    def normalize(dto: MailingInputDTO) -> MailingNormalizedDTO:
        def clean(value) -> str | None:
            if value is None:
                return None
            value = str(value).strip()
            return value if value != "" else None

        return MailingNormalizedDTO(
            # Básico
            nome=clean(dto.nome),
            email=clean(dto.email),
            telefone=clean(dto.telefone),
            origem=clean(dto.origem),
            tags=clean(dto.tags),

            # Datas e ingestão
            data_ingestao=clean(dto.data_ingestao),
            fonte_arquivo=clean(dto.fonte_arquivo),

            # Validação
            valido=dto.valido,
            motivo_invalidacao=clean(dto.motivo_invalidacao),
            hash_unico=clean(dto.hash_unico),

            # Perfil pessoal
            sexo=clean(dto.sexo),
            data_nascimento=clean(dto.data_nascimento),
            idade=dto.idade,
            estado_civil=clean(dto.estado_civil),
            nacionalidade=clean(dto.nacionalidade),
            profissao=clean(dto.profissao),
            empresa=clean(dto.empresa),
            cargo=clean(dto.cargo),
            renda_mensal=dto.renda_mensal,
            faixa_renda=clean(dto.faixa_renda),
            escolaridade=clean(dto.escolaridade),

            # Endereço
            cep=clean(dto.cep),
            logradouro=clean(dto.logradouro),
            numero=clean(dto.numero),
            complemento=clean(dto.complemento),
            bairro=clean(dto.bairro),
            cidade=clean(dto.cidade),
            estado=clean(dto.estado),
            pais=clean(dto.pais),

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
            primeiro_contato=clean(dto.primeiro_contato),
            ultimo_contato=clean(dto.ultimo_contato),
            canal_preferido=clean(dto.canal_preferido),
            score_mailing=dto.score_mailing
        )
