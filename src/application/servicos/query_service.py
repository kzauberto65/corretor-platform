from src.persistencia.repositorios.base_repository import BaseRepository
from src.ingestao.normalizador import Normalizador


class QueryService(BaseRepository):

    def __init__(self):
        super().__init__()
        self.normalizador = Normalizador()

    # =====================================================
    # BUSCA PAGINADA (RETORNA REGISTROS)
    # =====================================================
    def buscar_empreendimentos(
        self,
        cidade=None,
        regiao=None,
        tipologia=None,
        periodo_lancamento=None,
        status=None,
        preco_min=None,
        preco_max=None,
        ordenar_por=None,
        ordem="asc",
        pagina=1,
        por_pagina=10
    ):
        query = "SELECT * FROM empreendimentos WHERE 1=1"
        params = []

        cidade = self.normalizador.texto_busca(cidade)
        regiao = self.normalizador.texto_busca(regiao)
        tipologia = self.normalizador.texto_busca(tipologia)
        periodo_lancamento = self.normalizador.texto_busca(periodo_lancamento)
        status = self.normalizador.texto_busca(status)

        if cidade:
            query += " AND LOWER(cidade) LIKE ?"
            params.append(f"%{cidade}%")

        if regiao:
            query += " AND LOWER(regiao) LIKE ?"
            params.append(f"%{regiao}%")

        if tipologia:
            query += " AND LOWER(tipologia) LIKE ?"
            params.append(f"%{tipologia}%")

        if periodo_lancamento:
            query += " AND LOWER(periodo_lancamento) LIKE ?"
            params.append(f"%{periodo_lancamento}%")

        if status:
            query += " AND LOWER(status_entrega) LIKE ?"
            params.append(f"%{status}%")

        if preco_min is not None:
            query += " AND preco >= ?"
            params.append(preco_min)

        if preco_max is not None:
            query += " AND preco <= ?"
            params.append(preco_max)

        ordenacoes_permitidas = {
            "preco": "preco",
            "cidade": "cidade",
            "nome": "nome",
            "lancamento": "periodo_lancamento",
            "regiao": "regiao"
        }

        ordem = ordem.lower()
        if ordem not in ("asc", "desc"):
            ordem = "asc"

        if ordenar_por in ordenacoes_permitidas:
            coluna = ordenacoes_permitidas[ordenar_por]
            query += f" ORDER BY {coluna} {ordem.upper()}"

        pagina = max(1, int(pagina))
        por_pagina = max(1, int(por_pagina))
        offset = (pagina - 1) * por_pagina

        query += " LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])

        return self.fetch_all(query, tuple(params))

    # =====================================================
    # CONTAGEM TOTAL (RETORNA UM INTEIRO)
    # =====================================================
    def contar_empreendimentos(self, filtros):
        query = "SELECT COUNT(*) AS total FROM empreendimentos WHERE 1=1"
        params = []

        cidade = self.normalizador.texto_busca(filtros.get("cidade"))
        regiao = self.normalizador.texto_busca(filtros.get("regiao"))
        tipologia = self.normalizador.texto_busca(filtros.get("tipologia"))
        periodo_lancamento = self.normalizador.texto_busca(filtros.get("lancamento"))
        status = self.normalizador.texto_busca(filtros.get("status"))

        if cidade:
            query += " AND LOWER(cidade) LIKE ?"
            params.append(f"%{cidade}%")

        if regiao:
            query += " AND LOWER(regiao) LIKE ?"
            params.append(f"%{regiao}%")

        if tipologia:
            query += " AND LOWER(tipologia) LIKE ?"
            params.append(f"%{tipologia}%")

        if periodo_lancamento:
            query += " AND LOWER(periodo_lancamento) LIKE ?"
            params.append(f"%{periodo_lancamento}%")

        if status:
            query += " AND LOWER(status_entrega) LIKE ?"
            params.append(f"%{status}%")

        if filtros.get("preco_min") is not None:
            query += " AND preco >= ?"
            params.append(filtros["preco_min"])

        if filtros.get("preco_max") is not None:
            query += " AND preco <= ?"
            params.append(filtros["preco_max"])

        resultado = self.fetch_one(query, tuple(params))
        return resultado["total"]
