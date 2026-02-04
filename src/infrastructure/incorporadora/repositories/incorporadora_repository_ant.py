from src.persistencia.repositorios.base_repository import BaseRepository

class IncorporadoraRepository(BaseRepository):

    def criar_ou_obter(self, nome):
        existente = self.fetch_one(
            "SELECT * FROM incorporadora WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )
        if existente:
            return existente

        self.execute(
            "INSERT INTO incorporadora (nome) VALUES (?)",
            (nome,)
        )

        return self.fetch_one(
            "SELECT * FROM incorporadora WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )