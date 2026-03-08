# ============================================================
# REPOSITORY: UnidadeRepository
# Camada: infrastructure/unidade/repositories/
# Descrição: CRUD e consultas da tabela `unidades`.
#            Apenas acesso ao banco — zero regra de negócio.
#            Toda lógica fica no Service e Engine.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

import sqlite3
from typing import Optional
from src.domain.unidade.entities.unidade_entity import UnidadeEntity


class UnidadeRepository:

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        # Caminho padrão do banco — relativo à raiz do projeto
        # Em produção futura, receber via injeção de dependência ou variável de ambiente
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        """Abre conexão com FK habilitado.
        Usar sempre dentro de 'with' para garantir fechamento."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row   # acesso por nome de coluna (não por índice)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _row_to_entity(self, row: sqlite3.Row) -> UnidadeEntity:
        """Mapeia uma row do SQLite para UnidadeEntity.
        Centralizado aqui para não repetir em cada método.
        Usa nomes de coluna (row_factory) — imune a mudanças de ordem."""
        return UnidadeEntity(
            id=row["id"],
            empreendimento_id=row["empreendimento_id"],
            codigo_unidade=row["codigo_unidade"],
            preco=row["preco"],
            metragem=row["metragem"],
            dormitorios=row["dormitorios"],
            suites=row["suites"],
            vagas=row["vagas"],
            tipo_unidade=row["tipo_unidade"],
            andar=row["andar"],
            disponibilidade=row["disponibilidade"],
            descricao_unidade=row["descricao_unidade"],
            observacoes=row["observacoes"],
            created_at=row["created_at"]
        )

    # ----------------------------------------------------------
    # ESCRITA
    # ----------------------------------------------------------

    def cadastrar(self, entity: UnidadeEntity) -> UnidadeEntity:
        """Insere uma nova unidade no banco.
        Retorna a entity com o id gerado pelo banco."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO unidades (
                    empreendimento_id,
                    codigo_unidade,
                    preco,
                    metragem,
                    dormitorios,
                    suites,
                    vagas,
                    tipo_unidade,
                    andar,
                    disponibilidade,
                    descricao_unidade,
                    observacoes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entity.empreendimento_id,
                entity.codigo_unidade,
                entity.preco,
                entity.metragem,
                entity.dormitorios,
                entity.suites,
                entity.vagas,
                entity.tipo_unidade,
                entity.andar,
                entity.disponibilidade,
                entity.descricao_unidade,
                entity.observacoes
            ))
            entity.id = cur.lastrowid
        return entity

    def atualizar(self, entity: UnidadeEntity) -> UnidadeEntity:
        """Atualiza todos os campos de uma unidade existente.
        Requer entity.id válido."""
        with self._conn() as conn:
            conn.execute("""
                UPDATE unidades SET
                    empreendimento_id   = ?,
                    codigo_unidade      = ?,
                    preco               = ?,
                    metragem            = ?,
                    dormitorios         = ?,
                    suites              = ?,
                    vagas               = ?,
                    tipo_unidade        = ?,
                    andar               = ?,
                    disponibilidade     = ?,
                    descricao_unidade   = ?,
                    observacoes         = ?
                WHERE id = ?
            """, (
                entity.empreendimento_id,
                entity.codigo_unidade,
                entity.preco,
                entity.metragem,
                entity.dormitorios,
                entity.suites,
                entity.vagas,
                entity.tipo_unidade,
                entity.andar,
                entity.disponibilidade,
                entity.descricao_unidade,
                entity.observacoes,
                entity.id
            ))
        return entity

    def atualizar_disponibilidade(self, unidade_id: int, disponibilidade: str) -> bool:
        """Atualiza apenas o status de disponibilidade da unidade.
        Método dedicado para operações rápidas de venda/reserva.
        Valores aceitos: disponível / vendido / reservado"""
        with self._conn() as conn:
            conn.execute(
                "UPDATE unidades SET disponibilidade = ? WHERE id = ?",
                (disponibilidade, unidade_id)
            )
        return True

    def remover(self, unidade_id: int) -> bool:
        """Remove uma unidade pelo id.
        ATENÇÃO: verificar dependências em ia_score e matching antes de remover."""
        with self._conn() as conn:
            conn.execute("DELETE FROM unidades WHERE id = ?", (unidade_id,))
        return True

    # ----------------------------------------------------------
    # LEITURA — CONSULTAS GERAIS
    # ----------------------------------------------------------

    def buscar_por_id(self, unidade_id: int) -> Optional[UnidadeEntity]:
        """Busca uma unidade pelo id. Retorna None se não encontrada."""
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM unidades WHERE id = ?", (unidade_id,)
            ).fetchone()
        return self._row_to_entity(row) if row else None

    def consultar(self) -> list[UnidadeEntity]:
        """Retorna todas as unidades cadastradas.
        Para uso em CLI e relatórios — não usar no pipeline de IA
        (usar list_disponiveis para não processar vendidas)."""
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT * FROM unidades ORDER BY empreendimento_id, codigo_unidade"
            ).fetchall()
        return [self._row_to_entity(r) for r in rows]

    # ----------------------------------------------------------
    # LEITURA — CONSULTAS ESPECÍFICAS DO PIPELINE
    # ----------------------------------------------------------

    def list_by_empreendimento(self, empreendimento_id: int) -> list[UnidadeEntity]:
        """Retorna todas as unidades de um empreendimento.
        Usado pelo EmpreendimentoService e CLI de empreendimentos."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM unidades
                WHERE empreendimento_id = ?
                ORDER BY andar, codigo_unidade
            """, (empreendimento_id,)).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def list_disponiveis(self) -> list[UnidadeEntity]:
        """Retorna apenas unidades disponíveis para venda.
        Usado pelo Matching Engine e IA Engine — nunca processar
        unidades vendidas ou reservadas."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM unidades
                WHERE disponibilidade = 'disponível'
                ORDER BY preco
            """).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def list_disponiveis_by_empreendimento(self, empreendimento_id: int) -> list[UnidadeEntity]:
        """Retorna unidades disponíveis de um empreendimento específico.
        Usado quando o corretor quer ver o que ainda pode vender."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM unidades
                WHERE empreendimento_id = ?
                  AND disponibilidade = 'disponível'
                ORDER BY preco
            """, (empreendimento_id,)).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def list_all_for_ia(self) -> list[UnidadeEntity]:
        """Retorna todas as unidades disponíveis com dados completos
        para vetorização no IAEngine.
        Filtra apenas disponíveis e exige campos mínimos para vetorização:
        preco, metragem e tipo_unidade não podem ser nulos."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT * FROM unidades
                WHERE disponibilidade = 'disponível'
                  AND preco IS NOT NULL
                  AND metragem IS NOT NULL
                  AND tipo_unidade IS NOT NULL
                ORDER BY empreendimento_id
            """).fetchall()
        return [self._row_to_entity(r) for r in rows]

    def contar_by_empreendimento(self, empreendimento_id: int) -> dict:
        """Retorna contagem de unidades por status de disponibilidade.
        Útil para dashboard e relatórios de empreendimento."""
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT disponibilidade, COUNT(*) as total
                FROM unidades
                WHERE empreendimento_id = ?
                GROUP BY disponibilidade
            """, (empreendimento_id,)).fetchall()
        return {row["disponibilidade"]: row["total"] for row in rows}