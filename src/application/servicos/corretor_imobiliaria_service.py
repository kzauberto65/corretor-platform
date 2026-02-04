# arquivo: corretor_imobiliaria_service.py
from src.persistencia.repositorios.corretor_imobiliaria_repository import CorretorImobiliariaRepository

class CorretorImobiliariaService:
    def __init__(self):
        self.repo = CorretorImobiliariaRepository()

    def vincular(self, corretor_id, imobiliaria_id):
        if not corretor_id or not imobiliaria_id:
            raise ValueError("IDs de corretor e imobiliária são obrigatórios")

        # Evitar duplicidade usando método específico
        existente = self.repo.buscar_vinculo(corretor_id, imobiliaria_id)
        if existente:
            return existente

        # Criar vínculo
        self.repo.criar(corretor_id, imobiliaria_id)

        # Retornar o vínculo recém-criado
        return self.repo.buscar_vinculo(corretor_id, imobiliaria_id)

    def listar(self):
        return self.repo.listar()

    def listar_por_corretor(self, corretor_id):
        return self.repo.listar_por_corretor(corretor_id)

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.repo.listar_por_imobiliaria(imobiliaria_id)

    def desvincular(self, corretor_id, imobiliaria_id):
        # Verificar se o vínculo existe
        existente = self.repo.buscar_vinculo(corretor_id, imobiliaria_id)
        if not existente:
            raise ValueError("Vínculo entre corretor e imobiliária não encontrado")

        # Remover vínculo
        self.repo.remover(corretor_id, imobiliaria_id)
        return True