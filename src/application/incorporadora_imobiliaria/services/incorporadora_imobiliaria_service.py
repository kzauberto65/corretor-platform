from src.domain.incorporadora_imobiliaria.normalizers.incorporadora_imobiliaria_normalizer import IncorporadoraImobiliariaNormalizer
from src.domain.incorporadora_imobiliaria.entities.incorporadora_imobiliaria_entity import IncorporadoraImobiliariaEntity
from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_input_dto import IncorporadoraImobiliariaInputDTO


class IncorporadoraImobiliariaService:

    def __init__(self, repository):
        self.repository = repository

    def cadastrar(self, dto: IncorporadoraImobiliariaInputDTO):
        normalized = IncorporadoraImobiliariaNormalizer.normalize(dto)
        entity = IncorporadoraImobiliariaEntity(**normalized.__dict__)
        return self.repository.cadastrar(entity)

    def atualizar(self, dto: IncorporadoraImobiliariaInputDTO):
        normalized = IncorporadoraImobiliariaNormalizer.normalize(dto)
        entity = IncorporadoraImobiliariaEntity(**normalized.__dict__)
        return self.repository.atualizar(entity)

    def consultar(self):
        return self.repository.consultar()

    def buscar_por_ids(self, incorporadora_id: int, imobiliaria_id: int):
        return self.repository.buscar_por_ids(incorporadora_id, imobiliaria_id)

    def remover(self, incorporadora_id: int, imobiliaria_id: int):
        return self.repository.remover(incorporadora_id, imobiliaria_id)
