from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.domain.imobiliaria.dto.imobiliaria_normalized_dto import ImobiliariaNormalizedDTO

class ImobiliariaNormalizer:

    @staticmethod
    def normalize(input_dto: ImobiliariaInputDTO) -> ImobiliariaNormalizedDTO:

        def clean(value: str | None) -> str | None:
            if value is None:
                return None
            value = value.strip()
            return value if value else None

        def title(value: str | None) -> str | None:
            value = clean(value)
            return value.title() if value else None

        return ImobiliariaNormalizedDTO(
            nome=title(input_dto.nome),
            cnpj=clean(input_dto.cnpj),
            contato=clean(input_dto.contato),
            observacoes=clean(input_dto.observacoes),
        )
