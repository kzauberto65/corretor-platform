from src.persistencia.repositorios.base_repository import BaseRepository

class UnidadeReferenciaRepository(BaseRepository):
    def criar_ou_obter(self, nome):
        row = self.fetch_one(
            "SELECT id FROM unidades_referencia WHERE nome = ?",
            (nome,)
        )
        if row:
            return row["id"]

        self.execute(
            "INSERT INTO unidades_referencia (nome) VALUES (?)",
            (nome,)
        )
        return self.last_insert_id()