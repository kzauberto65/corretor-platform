from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO
from src.domain.construtora.dto.construtora_normalized_dto import ConstrutoraNormalizedDTO

class ConstrutoraNormalizer:

    @staticmethod
    def normalize(dto: ConstrutoraInputDTO) -> ConstrutoraNormalizedDTO:
        def clean(value: str | None) -> str | None:
            if value is None:
                return None
            value = value.strip()
            return value if value != "" else None

        return ConstrutoraNormalizedDTO(
            nome=clean(dto.nome),
            cnpj=clean(dto.cnpj),
            contato=clean(dto.contato),
            observacoes=clean(dto.observacoes),
            fonte=clean(dto.fonte),
            data_registro=clean(dto.data_registro),
            usuario_id=clean(dto.usuario_id),
            justificativa=clean(dto.justificativa)
        )
