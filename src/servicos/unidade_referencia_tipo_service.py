# arquivo: unidade_referencia_tipo_service.py
from src.persistencia.repositorios.unidade_referencia_tipo_repository import UnidadeReferenciaTipoRepository

class UnidadeReferenciaTipoService:
    def __init__(self):
        self.repo = UnidadeReferenciaTipoRepository()

    def criar_ou_obter(self, nome):
        if not nome or nome.strip() == "":
            raise ValueError("O nome do tipo de unidade é obrigatório")

        return self.repo.criar_ou_obter(nome)

    def listar_tipos(self):
        return self.repo.listar()

    def buscar_por_id(self, tipo_id):
        return self.repo.buscar_por_id(tipo_id)

    def remover_tipo(self, tipo_id):
        existente = self.repo.buscar_por_id(tipo_id)
        if not existente:
            raise ValueError("Tipo de unidade não encontrado")

        self.repo.remover(tipo_id)
        return True