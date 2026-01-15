# src/persistencia/repositorios/construtora_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class ConstrutoraRepository(BaseRepository):
    def criar(self, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        INSERT INTO construtoras (nome, cnpj, contato, observacoes)
        VALUES (?, ?, ?, ?)
        """
        self.execute(query, (nome, cnpj, contato, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM construtoras")