# arquivo: imobiliaria_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class ImobiliariaRepository(BaseRepository):

    def criar(self, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        INSERT INTO imobiliarias (
            nome,
            cnpj,
            contato,
            observacoes
        )
        VALUES (?, ?, ?, ?)
        """
        self.execute(query, (nome, cnpj, contato, observacoes))

    def listar(self):
        return self.fetch_all("SELECT * FROM imobiliarias")

    def buscar_por_id(self, imobiliaria_id):
        return self.fetch_one(
            "SELECT * FROM imobiliarias WHERE id = ?",
            (imobiliaria_id,)
        )

    def buscar_por_nome(self, nome):
        return self.fetch_one(
            "SELECT * FROM imobiliarias WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )

    def atualizar(self, imobiliaria_id, nome, cnpj=None, contato=None, observacoes=None):
        query = """
        UPDATE imobiliarias
        SET
            nome = ?,
            cnpj = ?,
            contato = ?,
            observacoes = ?
        WHERE id = ?
        """
        self.execute(
            query,
            (nome, cnpj, contato, observacoes, imobiliaria_id)
        )

    def remover(self, imobiliaria_id):
        self.execute(
            "DELETE FROM imobiliarias WHERE id = ?",
            (imobiliaria_id,)
        )