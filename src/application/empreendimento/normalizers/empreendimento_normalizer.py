from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_normalized_dto import EmpreendimentoNormalizedDTO

class EmpreendimentoNormalizer:

    @staticmethod
    def normalize(input_dto: EmpreendimentoInputDTO) -> EmpreendimentoNormalizedDTO:

        def clean(value: str | None) -> str | None:
            if value is None:
                return None
            value = value.strip()
            return value if value else None

        def title(value: str | None) -> str | None:
            value = clean(value)
            return value.title() if value else None

        return EmpreendimentoNormalizedDTO(
            regiao=title(input_dto.regiao),
            bairro=title(input_dto.bairro),
            cidade=title(input_dto.cidade),
            estado=title(input_dto.estado),
            produto=title(input_dto.produto),
            endereco=clean(input_dto.endereco),
            data_entrega=clean(input_dto.data_entrega),
            status_entrega=title(input_dto.status_entrega),
            tipo=title(input_dto.tipo),
            descricao=clean(input_dto.descricao),
            preco=input_dto.preco,
            proprietario_id=input_dto.proprietario_id,
            incorporadora_id=input_dto.incorporadora_id,
            unidade_referencia_id=input_dto.unidade_referencia_id,
            spe_id=input_dto.spe_id,
            periodo_lancamento=clean(input_dto.periodo_lancamento),
            nome=title(input_dto.nome),
            tipologia=title(input_dto.tipologia),
        )
