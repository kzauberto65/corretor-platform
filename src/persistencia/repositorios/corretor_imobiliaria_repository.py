# arquivo: corretor_imobiliaria_repository.py
from src.persistencia.repositorios.base_repository import BaseRepository

class CorretorImobiliariaRepository(BaseRepository):

    def criar(self, corretor_id, imobiliaria_id):
        query = """
        INSERT INTO corretor_imobiliaria (
            corretor_id,
            imobiliaria_id
        )
        VALUES (?, ?)
        """
        self.execute(query, (corretor_id, imobiliaria_id))

    def listar(self):
        return self.fetch_all("SELECT * FROM corretor_imobiliaria")

    def listar_por_corretor(self, corretor_id):
        return self.fetch_all(
            "SELECT * FROM corretor_imobiliaria WHERE corretor_id = ?",
            (corretor_id,)
        )

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.fetch_all(
            "SELECT * FROM corretor_imobiliaria WHERE imobiliaria_id = ?",
            (imobiliaria_id,)
        )

    def buscar_vinculo(self, corretor_id, imobiliaria_id):
        return self.fetch_one(
            """
            SELECT *
            FROM corretor_imobiliaria
            WHERE corretor_id = ? AND imobiliaria_id = ?
            """,
            (corretor_id, imobiliaria_id)
        )

    def remover(self, corretor_id, imobiliaria_id):
        self.execute(
            """
            DELETE FROM corretor_imobiliaria
            WHERE corretor_id = ? AND imobiliaria_id = ?
            """,
            (corretor_id, imobiliaria_id)
        )