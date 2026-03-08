# ============================================================
# REPOSITORY: EmpreendimentoRepository
# Camada: infrastructure/empreendimento/repositories/
# Descrição: CRUD e consultas da tabela `empreendimentos`.
#            Apenas acesso ao banco — zero regra de negócio,
#            zero normalização (papel do Normalizer na application).
#            Empreendimento = contexto institucional (Sprint 10.5).
#            Filtros de preco/metragem foram removidos — esses dados
#            agora vivem em unidades e devem ser filtrados lá.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

import sqlite3
from typing import Optional
from src.domain.empreendimento.entities.empreendimento_entity import EmpreendimentoEntity


class EmpreendimentoRepository:

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        """Abre conexão com FK habilitado e row_factory por nome de coluna."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _row_to_entity(self, row: sqlite3.Row) -> EmpreendimentoEntity:
        """Mapeia row do SQLite para EmpreendimentoEntity pelo nome da coluna.
        Imune a mudanças de ordem no schema."""
        return EmpreendimentoEntity(
            id=row["id"],
            nome=row["nome"],
            regiao=row["regiao"],
            bairro=row["bairro"],
            cidade=row["cidade"],
            estado=row["estado"],
            endereco=row["endereco"],
            produto=row["produto"],
            tipo=row["tipo"],
            descricao=row["descricao"],
            periodo_lancamento=row["periodo_lancamento"],
            data_entrega=row["data_entrega"],
            status_entrega=row["status_entrega"],
            total_unidades=row["total_unidades"],
            amenities=row["amenities"],
            padrao_construtivo=row["padrao_construtivo"],
            incorporadora_id=row["incorporadora_id"],
            proprietario_id=row["proprietario_id"],
            spe_id=row["spe_id"],
            unidade_referencia_id=row["unidade_referencia_id"]
        )

    # ----------------------------------------------------------
    # ESCRITA
    # ----------------------------------------------------------

    def save(self, entity: EmpreendimentoEntity) -> EmpreendimentoEntity:
        """Insere um novo empreendimento no banco.
        Retorna a entity com o id gerado."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO empreendimentos (
                    nome, regiao, bairro, cidade, estado, endereco,
                    produto, tipo, descricao, periodo_lancamento,
                    data_entrega, status_entrega, total_unidades,
                    amenities, padrao_construtivo,
                    incorporadora_id, proprietario_id, spe_id,
                    unidade_referencia_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity.nome, entity.regiao, entity.bairro,
                entity.cidade, entity.estado, entity.endereco,
                entity.produto, entity.tipo, entity.descricao,
                entity.periodo_lancamento, entity.data_entrega,
                entity.status_entrega, entity.total_unidades,
                entity.amenities, entity.padrao_construtivo,
                entity.incorporadora_id, entity.proprietario_id,
                entity.spe_id, entity.unidade_referencia_id
            ))
            entity.id = cur.lastrowid
        return entity

    def update(self, entity: EmpreendimentoEntity) -> EmpreendimentoEntity:
        """Atualiza todos os campos de um empreendimento existente."""
        with self._conn() as conn:
            conn.execute("""
                UPDATE empreendimentos SET
                    nome                = ?,
                    regiao              = ?,
                    bairro              = ?,
                    cidade              = ?,
                    estado              = ?,
                    endereco            = ?,
                    produto             = ?,
                    tipo                = ?,
                    descricao           = ?,
                    periodo_lancamento  = ?,
                    data_entrega        = ?,
                    status_entrega      = ?,
                    total_unidades      = ?,
                    amenities           = ?,
                    padrao_construtivo  = ?,
                    incorporadora_id    = ?,
                    proprietario_id     = ?,
                    spe_id              = ?,
                    unidade_referencia_id = ?
                WHERE id = ?
            """, (
                entity.nome, entity.regiao, entity.bairro,
                entity.cidade, entity.estado, entity.endereco,
                entity.produto, entity.tipo, entity.descricao,
                entity.periodo_lancamento, entity.data_entrega,
                entity.status_entrega, entity.total_unidades,
                entity.amenities, entity.padrao_construtivo,
                entity.incorporadora_id, entity.proprietario_id,
                entity.spe_id, entity.unidade_referencia_id,
                entity.id
            ))
        return entity

    def delete(self, empreendimento_id: int) -> bool:
        """Remove um empreendimento pelo id.
        ATENÇÃO: verificar unidades vinculadas antes de remover
        (FK em unidades.empreendimento_id vai bloquear se houver unidades)."""
        with self._conn() as conn:
            conn.execute(
                "DELETE FROM empreendimentos WHERE id = ?",
                (empreendimento_id,)
            )
        return True

    # ----------------------------------------------------------
    # LEITURA — CONSULTAS GERAIS
    # ----------------------------------------------------------

    def find_by_id(self, empreendimento_id: int) -> Optional[EmpreendimentoEntity]:
        """Busca empreendimento pelo id. Retorna None se não encontrado."""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM empreendimentos WHERE id = ?",
                (empreendimento_id,)
            ).fetchone()
        return self._row_to_entity(row) if row else None

    def find(self) -> list[EmpreendimentoEntity]:
        """Retorna todos os empreendimentos cadastrados.
        Para uso administrativo — sem filtros."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM empreendimentos ORDER BY nome"
            ).fetchall()
        return [self._row_to_entity(r) for r in rows]

    # ----------------------------------------------------------
    # LEITURA — CONSULTAS FILTRADAS
    # Filtros válidos pós-Sprint 10.5: localização, status, período
    # Filtros de preco/metragem → usar UnidadeRepository
    # ----------------------------------------------------------

    def find_filtered(
        self,
        cidade: Optional[str] = None,
        regiao: Optional[str] = None,
        status_entrega: Optional[str] = None,
        periodo_lancamento: Optional[str] = None,
        incorporadora_id: Optional[int] = None,
        ordenar_por: Optional[str] = None,
        ordem: str = "asc",
        pagina: int = 1,
        por_pagina: int = 999999
    ) -> list[EmpreendimentoEntity]:
        """Consulta empreendimentos com filtros opcionais.

        ATENÇÃO: filtros de preco e metragem foram removidos (Sprint 10.5).
        Para filtrar por preco/metragem usar UnidadeRepository.list_disponiveis()
        e filtrar na camada de serviço.

        Filtros disponíveis:
          cidade, regiao          → LIKE (parcial, case-insensitive)
          status_entrega          → LIKE (ex: 'em obras', 'entregue')
          periodo_lancamento      → LIKE (ex: 'Q1/2025')
          incorporadora_id        → exato
        """
        query = "SELECT * FROM empreendimentos WHERE 1=1"
        params = []

        # Filtros textuais — case-insensitive com LIKE
        if cidade:
            query += " AND LOWER(cidade) LIKE ?"
            params.append(f"%{cidade.strip().lower()}%")

        if regiao:
            query += " AND LOWER(regiao) LIKE ?"
            params.append(f"%{regiao.strip().lower()}%")

        if status_entrega:
            query += " AND LOWER(status_entrega) LIKE ?"
            params.append(f"%{status_entrega.strip().lower()}%")

        if periodo_lancamento:
            query += " AND LOWER(periodo_lancamento) LIKE ?"
            params.append(f"%{periodo_lancamento.strip().lower()}%")

        # Filtro exato por incorporadora
        if incorporadora_id:
            query += " AND incorporadora_id = ?"
            params.append(incorporadora_id)

        # Ordenação segura — apenas colunas permitidas
        colunas_ordenacao = {
            "nome": "nome",
            "cidade": "cidade",
            "regiao": "regiao",
            "lancamento": "periodo_lancamento",
            "entrega": "data_entrega",
            "status": "status_entrega"
        }
        ordem = ordem.lower() if ordem.lower() in ("asc", "desc") else "asc"
        if ordenar_por in colunas_ordenacao:
            coluna = colunas_ordenacao[ordenar_por]
            query += f" ORDER BY {coluna} {ordem.upper()}"
        else:
            query += " ORDER BY nome ASC"

        # Paginação
        pagina = max(1, int(pagina))
        por_pagina = max(1, int(por_pagina))
        offset = (pagina - 1) * por_pagina
        query += " LIMIT ? OFFSET ?"
        params.extend([por_pagina, offset])

        with self._conn() as conn:
            rows = conn.execute(query, params).fetchall()
        return [self._row_to_entity(r) for r in rows]

    # ----------------------------------------------------------
    # LEITURA — CONSULTAS ESPECÍFICAS DO PIPELINE
    # ----------------------------------------------------------

    def find_by_cidade(self, cidade: str) -> list[EmpreendimentoEntity]:
        """Retorna empreendimentos de uma cidade específica.
        Usado pelo pipeline de matching e IA para filtrar por localização."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM empreendimentos
                WHERE LOWER(cidade) LIKE ?
                ORDER BY nome
            """, (f"%{cidade.strip().lower()}%",)).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def find_by_incorporadora(self, incorporadora_id: int) -> list[EmpreendimentoEntity]:
        """Retorna todos os empreendimentos de uma incorporadora.
        Útil para relatórios por incorporadora."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM empreendimentos
                WHERE incorporadora_id = ?
                ORDER BY nome
            """, (incorporadora_id,)).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def find_disponiveis(self) -> list[EmpreendimentoEntity]:
        """Retorna empreendimentos que ainda têm unidades disponíveis.
        Faz JOIN com unidades para verificar disponibilidade real.
        Usado pelo pipeline de oferta e matching."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT DISTINCT e.*
                FROM empreendimentos e
                INNER JOIN unidades u ON u.empreendimento_id = e.id
                WHERE u.disponibilidade = 'disponível'
                ORDER BY e.nome
            """).fetchall()
        return [self._row_to_entity(r) for r in rows]