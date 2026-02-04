from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.domain.imobiliaria.dto.imobiliaria_dto import ImobiliariaDTO
from src.application.imobiliaria.normalizers.imobiliaria_normalizer import ImobiliariaNormalizer
from src.domain.imobiliaria.entities.imobiliaria_entity import ImobiliariaEntity

class ImobiliariaService:

    def __init__(self, repo):
        self.repo = repo

    def cadastrar(self, input_dto: ImobiliariaInputDTO) -> ImobiliariaDTO:
        normalized = ImobiliariaNormalizer.normalize(input_dto)
        entity = ImobiliariaEntity(id=None, **normalized.__dict__)
        dto = ImobiliariaDTO(**entity.to_dict())
        return self.repo.save(dto)

    def atualizar(self, id: int, input_dto: ImobiliariaInputDTO):
        existente = self.repo.find_by_id(id)
        if not existente:
            return None
        normalized = ImobiliariaNormalizer.normalize(input_dto)
        atualizado = ImobiliariaDTO(id=id, **normalized.__dict__)
        return self.repo.update(atualizado)

    def consultar(self):
        return self.repo.find()

    def buscar_por_id(self, id: int):
        return self.repo.find_by_id(id)

    def remover(self, id: int):
        self.repo.delete(id)
        return True
