from src.persistencia.repositorios.unidade_referencia_repository import UnidadeReferenciaRepository

class UnidadeReferenciaService:
    def __init__(self):
        self.repo = UnidadeReferenciaRepository()

    def criar_ou_obter(self, nome):
        return self.repo.criar_ou_obter(nome)