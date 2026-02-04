from src.domain.corretor_unidade.normalizers.corretor_unidade_normalizer import CorretorUnidadeNormalizer
from src.domain.corretor_unidade.entities.corretor_unidade_entity import CorretorUnidadeEntity
from src.domain.corretor_unidade.dto.corretor_unidade_input_dto import CorretorUnidadeInputDTO


class CorretorUnidadeService:

    def __init__(self, repository):
        self.repository = repository

    def cadastrar(self, dto: CorretorUnidadeInputDTO):
        normalized = CorretorUnidadeNormalizer.normalize(dto)
        entity = CorretorUnidadeEntity(**normalized.__dict__)
        return self.repository.cadastrar(entity)

    def atualizar(self, dto: CorretorUnidadeInputDTO):
        normalized = CorretorUnidadeNormalizer.normalize(dto)
        entity = CorretorUnidadeEntity(**normalized.__dict__)
        return self.repository.atualizar(entity)

    def consultar(self):
        return self.repository.consultar()

    def buscar_por_ids(self, corretor_id: int, unidade_id: int):
        return self.repository.buscar_por_ids(corretor_id, unidade_id)

    def remover(self, corretor_id: int, unidade_id: int):
        return self.repository.remover(corretor_id, unidade_id)
