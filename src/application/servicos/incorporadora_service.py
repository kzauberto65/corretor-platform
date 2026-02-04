from src.persistencia.repositorios.incorporadora_repository import IncorporadoraRepository

class IncorporadoraService:
    def __init__(self):
        self.repo = IncorporadoraRepository()

    def criar_ou_obter(self, nome):
        return self.repo.criar_ou_obter(nome)