# arquivo: construtora_imobiliaria_service.py
from src.persistencia.repositorios.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository

class ConstrutoraImobiliariaService:
    def __init__(self):
        self.repo = ConstrutoraImobiliariaRepository()

    def vincular(self, construtora_id, imobiliaria_id):
        if not construtora_id or not imobiliaria_id:
            raise ValueError("IDs de construtora e imobiliária são obrigatórios")

        # Evitar duplicidade usando método específico
        existente = self.repo.buscar_vinculo(construtora_id, imobiliaria_id)
        if existente:
            return existente

        # Criar vínculo
        self.repo.criar(construtora_id, imobiliaria_id)

        # Retornar o vínculo recém-criado
        return self.repo.buscar_vinculo(construtora_id, imobiliaria_id)

    def listar(self):
        return self.repo.listar()

    def listar_por_construtora(self, construtora_id):
        return self.repo.listar_por_construtora(construtora_id)

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.repo.listar_por_imobiliaria(imobiliaria_id)

    def desvincular(self, construtora_id, imobiliaria_id):
        # Verificar se o vínculo existe
        existente = self.repo.buscar_vinculo(construtora_id, imobiliaria_id)
        if not existente:
            raise ValueError("Vínculo entre construtora e imobiliária não encontrado")

        # Remover vínculo
        self.repo.remover(construtora_id, imobiliaria_id)
        return True