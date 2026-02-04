from src.domain.importacao.dto.importacao_input_dto import ImportacaoInputDTO
from src.domain.importacao.dto.importacao_normalized_dto import ImportacaoNormalizedDTO

class ImportacaoNormalizer:

    @staticmethod
    def normalize(dto: ImportacaoInputDTO) -> ImportacaoNormalizedDTO:
        def clean(value):
            if value is None:
                return None
            if isinstance(value, str):
                value = value.strip()
                return value if value != "" else None
            return value

        return ImportacaoNormalizedDTO(
            tipo=clean(dto.tipo),
            arquivo=clean(dto.arquivo),
            origem=clean(dto.origem),
            total_registros=clean(dto.total_registros),
            status=clean(dto.status),
            data_execucao=clean(dto.data_execucao),
            sucesso=clean(dto.sucesso),
            erros=clean(dto.erros),
            log=clean(dto.log)
        )
