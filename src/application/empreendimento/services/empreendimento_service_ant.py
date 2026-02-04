from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO
from src.application.empreendimento.normalizers.empreendimento_normalizer import EmpreendimentoNormalizer
from src.domain.empreendimento.entities.empreendimento_entity import EmpreendimentoEntity

class EmpreendimentoService:

    def __init__(self, repo):
        self.repo = repo

    def cadastrar(self, input_dto: EmpreendimentoInputDTO) -> EmpreendimentoDTO:
        normalized = EmpreendimentoNormalizer.normalize(input_dto)
        entity = EmpreendimentoEntity(id=None, **normalized.__dict__)
        dto = EmpreendimentoDTO(**entity.to_dict())
        return self.repo.save(dto)

    def atualizar(self, id: int, input_dto: EmpreendimentoInputDTO):
        existente = self.repo.find_by_id(id)
        if not existente:
            return None

        normalized = EmpreendimentoNormalizer.normalize(input_dto)
        atualizado = EmpreendimentoDTO(id=id, **normalized.__dict__)
        return self.repo.update(atualizado)

    def consultar(self):
        return self.repo.find()

    def buscar_por_id(self, id: int):
        return self.repo.find_by_id(id)

    def remover(self, id: int):
        self.repo.delete(id)
        return True
