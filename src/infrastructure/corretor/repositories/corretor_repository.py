# ============================================================
# REPOSITORY: CorretorRepository
# Camada: infrastructure/corretor/repositories/
# Descrição: Operações de persistência para Corretor.
#            Implementa CRUD básico com SQLite.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

import sqlite3
from typing import List, Optional
from src.domain.corretor.entities.corretor_entity import CorretorEntity


class CorretorRepository:

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão configurada."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome (row['nome'])
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_db(self):
        """Garante que a tabela exista."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS corretores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    creci TEXT,
                    observacoes TEXT
                )
            """)

    # ----------------------------------------------------------
    # MAPPER (Obrigatório pela arquitetura)
    # ----------------------------------------------------------
    def _row_to_entity(self, row: sqlite3.Row) -> CorretorEntity:
        """Converte uma linha do banco de dados (sqlite3.Row) para a Entity."""
        return CorretorEntity(
            id=row["id"],
            nome=row["nome"],
            telefone=row["telefone"],
            email=row["email"],
            creci=row["creci"],
            observacoes=row["observacoes"]
        )

    # ----------------------------------------------------------
    # OPERAÇÕES CRUD PADRONIZADAS
    # ----------------------------------------------------------
    def save(self, entity: CorretorEntity) -> CorretorEntity:
        """Salva a entidade. Faz INSERT se id for None, ou UPDATE se id existir."""
        with self._get_connection() as conn:
            if entity.id is None:
                cursor = conn.execute("""
                    INSERT INTO corretores (nome, telefone, email, creci, observacoes)
                    VALUES (?, ?, ?, ?, ?)
                """, (entity.nome, entity.telefone, entity.email, entity.creci, entity.observacoes))
                entity.id = cursor.lastrowid
            else:
                conn.execute("""
                    UPDATE corretores SET
                        nome = ?, telefone = ?, email = ?, creci = ?, observacoes = ?
                    WHERE id = ?
                """, (entity.nome, entity.telefone, entity.email, entity.creci, entity.observacoes, entity.id))
        return entity

    def find(self) -> List[CorretorEntity]:
        """Retorna todos os corretores cadastrados."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM corretores")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]

    def find_by_id(self, corretor_id: int) -> Optional[CorretorEntity]:
        """Busca um corretor pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM corretores WHERE id = ?", (corretor_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_entity(row)
            return None

    def delete(self, corretor_id: int) -> bool:
        """Remove um corretor pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM corretores WHERE id = ?", (corretor_id,))
            return cursor.rowcount > 0