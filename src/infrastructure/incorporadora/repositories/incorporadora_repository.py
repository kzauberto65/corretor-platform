# ============================================================
# REPOSITORY: IncorporadoraRepository
# Camada: infrastructure/incorporadora/repositories/
# Descrição: Operações de persistência para Incorporadora.
#            Implementa CRUD unificado com SQLite.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

import sqlite3
from typing import List, Optional
from src.domain.incorporadora.entities.incorporadora_entity import IncorporadoraEntity


class IncorporadoraRepository:

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão configurada."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        """Garante que a tabela exista antes de qualquer operação."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS incorporadora (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT,
                    reputacao TEXT,
                    historico_obra TEXT
                )
            """)

    # ----------------------------------------------------------
    # MAPPER (Exigido pela arquitetura)
    # ----------------------------------------------------------
    def _row_to_entity(self, row: sqlite3.Row) -> IncorporadoraEntity:
        """Converte uma linha do banco de dados na Entidade Incorporadora."""
        return IncorporadoraEntity(
            id=row["id"],
            nome=row["nome"],
            cnpj=row["cnpj"],
            reputacao=row["reputacao"],
            historico_obra=row["historico_obra"]
        )

    # ----------------------------------------------------------
    # OPERAÇÕES CRUD PADRONIZADAS
    # ----------------------------------------------------------
    def save(self, entity: IncorporadoraEntity) -> IncorporadoraEntity:
        """
        Salva a entidade. 
        Faz INSERT se o ID for None, caso contrário faz UPDATE.
        """
        with self._get_connection() as conn:
            if entity.id is None:
                cursor = conn.execute("""
                    INSERT INTO incorporadora (nome, cnpj, reputacao, historico_obra)
                    VALUES (?, ?, ?, ?)
                """, (entity.nome, entity.cnpj, entity.reputacao, entity.historico_obra))
                entity.id = cursor.lastrowid
            else:
                conn.execute("""
                    UPDATE incorporadora SET 
                        nome = ?, cnpj = ?, reputacao = ?, historico_obra = ?
                    WHERE id = ?
                """, (entity.nome, entity.cnpj, entity.reputacao, entity.historico_obra, entity.id))
        return entity

    def find(self) -> List[IncorporadoraEntity]:
        """Retorna todas as incorporadoras."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM incorporadora")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]

    def find_by_id(self, incorporadora_id: int) -> Optional[IncorporadoraEntity]:
        """Busca incorporadora pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM incorporadora WHERE id = ?", (incorporadora_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_entity(row)
            return None

    def delete(self, incorporadora_id: int) -> bool:
        """Remove a incorporadora pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM incorporadora WHERE id = ?", (incorporadora_id,))
            return cursor.rowcount > 0