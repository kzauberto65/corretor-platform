import sqlite3
from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO
from src.infrastructure.ingestao.normalizador import Normalizador


class EmpreendimentoRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path
        self.normalizador = Normalizador()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # ---------------------------------------------------------
    # CONSULTA COM FILTROS (CORRIGIDO)
    # ---------------------------------------------------------
    def find_filtered(
        self,
        cidade=None,
        regiao=None,
        metragem_min=None,
        metragem_max=None,
        lancamento=None,
        status=None,
        preco_min=None,
        preco_max=None,
        ordenar_por=None,
        ordem="asc",
        pagina=1,
        por_pagina=999999
    ):
        conn = self._conn()
        cur = conn.cursor()

        query = "SELECT * FROM empreendimentos WHERE 1=1"
        params = []

        cidade = self.normalizador.texto_busca(cidade)
        regiao = self.normalizador.texto_busca(regiao)
        lancamento = self.normalizador.texto_busca(lancamento)
        status = self.normalizador.texto_busca(status)

        if cidade:
            query += " AND LOWER(cidade) LIKE ?"
            params.append(f"%{cidade}%")

        if regiao:
            query += " AND LOWER(regiao) LIKE ?"
            params.append(f"%{regiao}%")

        # ---------------------------------------------------------
        # FILTRO POR METRAGEM (FAIXA COMPLETA DENTRO DO INTERVALO)
        # ---------------------------------------------------------
        if metragem_min is not None:
            query += " AND CAST(metragem_min AS REAL) >= ?"
            params.append(metragem_min)

        if metragem_max is not None:
            query += " AND CAST(metragem_max AS REAL) <= ?"
            params.append(metragem_max)

        if lancamento:
            query += " AND LOWER(periodo_lancamento) LIKE ?"
            params.append(f"%{lancamento}%")

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

        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        return [EmpreendimentoDTO(**dict(r)) for r in rows]

    # ---------------------------------------------------------
    # CONSULTA SIMPLES
    # ---------------------------------------------------------
    def find(self):
        return self.find_filtered()

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------
    def save(self, dto: EmpreendimentoDTO) -> EmpreendimentoDTO:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO empreendimentos (
                regiao, bairro, cidade, estado, produto, endereco,
                data_entrega, status_entrega, tipo, descricao, preco,
                proprietario_id, incorporadora_id, unidade_referencia_id,
                spe_id, periodo_lancamento, nome, tipologia,
                metragem_min, metragem_max
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dto.regiao, dto.bairro, dto.cidade, dto.estado, dto.produto,
            dto.endereco, dto.data_entrega, dto.status_entrega, dto.tipo,
            dto.descricao, dto.preco, dto.proprietario_id,
            dto.incorporadora_id, dto.unidade_referencia_id, dto.spe_id,
            dto.periodo_lancamento, dto.nome, dto.tipologia,
            dto.metragem_min, dto.metragem_max
        ))
        dto.id = cur.lastrowid
        conn.commit()
        conn.close()
        return dto

    def find_by_id(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM empreendimentos WHERE id = ?", (id,))
        r = cur.fetchone()
        conn.close()
        return EmpreendimentoDTO(**dict(r)) if r else None

    def update(self, dto: EmpreendimentoDTO):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE empreendimentos SET
                regiao = ?, bairro = ?, cidade = ?, estado = ?, produto = ?,
                endereco = ?, data_entrega = ?, status_entrega = ?, tipo = ?,
                descricao = ?, preco = ?, proprietario_id = ?, incorporadora_id = ?,
                unidade_referencia_id = ?, spe_id = ?, periodo_lancamento = ?,
                nome = ?, tipologia = ?, metragem_min = ?, metragem_max = ?
            WHERE id = ?
        """, (
            dto.regiao, dto.bairro, dto.cidade, dto.estado, dto.produto,
            dto.endereco, dto.data_entrega, dto.status_entrega, dto.tipo,
            dto.descricao, dto.preco, dto.proprietario_id,
            dto.incorporadora_id, dto.unidade_referencia_id, dto.spe_id,
            dto.periodo_lancamento, dto.nome, dto.tipologia,
            dto.metragem_min, dto.metragem_max,
            dto.id
        ))
        conn.commit()
        conn.close()
        return dto

    def delete(self, id: int):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM empreendimentos WHERE id = ?", (id,))
        conn.commit()
        conn.close()
