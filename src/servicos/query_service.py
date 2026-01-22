from src.persistencia.repositorios.base_repository import BaseRepository


class QueryService(BaseRepository):

    def buscar_empreendimentos(
        self,
        cidade=None,
        regiao=None,
        tipologia=None,
        periodo_lancamento=None,
        status=None,
        preco_min=None,
        preco_max=None
    ):
        query = "SELECT * FROM empreendimentos WHERE 1=1"
        params = []

        if cidade:
            query += " AND LOWER(cidade) LIKE LOWER(?)"
            params.append(f"%{cidade}%")

        if regiao:
            query += " AND LOWER(regiao) LIKE LOWER(?)"
            params.append(f"%{regiao}%")

        if tipologia:
            query += " AND LOWER(tipologia) LIKE LOWER(?)"
            params.append(f"%{tipologia}%")

        if periodo_lancamento:
            query += " AND LOWER(periodo_lancamento) LIKE LOWER(?)"
            params.append(f"%{periodo_lancamento}%")

        if status:
            query += " AND LOWER(status_entrega) LIKE LOWER(?)"
            params.append(f"%{status}%")

        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)

        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)

        return self.fetch_all(query, tuple(params))
