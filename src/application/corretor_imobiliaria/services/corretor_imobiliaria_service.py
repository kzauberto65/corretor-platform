from src.domain.corretor_imobiliaria.normalizers.corretor_imobiliaria_normalizer import CorretorImobiliariaNormalizer
from src.domain.corretor_imobiliaria.entities.corretor_imobiliaria_entity import CorretorImobiliariaEntity
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO


class CorretorImobiliariaService:

    def __init__(self, repository):
        self.repository = repository

    def cadastrar(self, dto: CorretorImobiliariaInputDTO):
        normalized = CorretorImobiliariaNormalizer.normalize(dto)
        entity = CorretorImobiliariaEntity(**normalized.__dict__)
        return self.repository.cadastrar(entity)

    def atualizar(self, dto: CorretorImobiliariaInputDTO):
        normalized = CorretorImobiliariaNormalizer.normalize(dto)
        entity = CorretorImobiliariaEntity(**normalized.__dict__)
        return self.repository.atualizar(entity)

    def consultar(self):
        return self.repository.consultar()

    def buscar_por_ids(self, corretor_id: int, imobiliaria_id: int):
        return self.repository.buscar_por_ids(corretor_id, imobiliaria_id)

    def remover(self, corretor_id: int, imobiliaria_id: int):
        return self.repository.remover(corretor_id, imobiliaria_id)
