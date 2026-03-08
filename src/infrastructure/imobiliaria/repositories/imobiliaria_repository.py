# ============================================================
# REPOSITORY: ImobiliariaRepository
# Camada: infrastructure/imobiliaria/repositories/
# Descrição: Operações de persistência para Imobiliaria.
#            Implementa CRUD unificado com SQLite.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

import sqlite3
from typing import List, Optional
from src.domain.imobiliaria.entities.imobiliaria_entity import ImobiliariaEntity


class ImobiliariaRepository:

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
        """Garante que a tabela exista antes de qualquer operação."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS imobiliarias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    cnpj TEXT,
                    contato TEXT,
                    observacoes TEXT
                )
            """)

    # ----------------------------------------------------------
    # MAPPER (Obrigatório pela arquitetura)
    # ----------------------------------------------------------
    def _row_to_entity(self, row: sqlite3.Row) -> ImobiliariaEntity:
        """Converte uma linha do banco de dados para a ImobiliariaEntity."""
        return ImobiliariaEntity(
            id=row["id"],
            nome=row["nome"],
            cnpj=row["cnpj"],
            contato=row["contato"],
            observacoes=row["observacoes"]
        )

    # ----------------------------------------------------------
    # OPERAÇÕES CRUD PADRONIZADAS
    # ----------------------------------------------------------
    def save(self, entity: ImobiliariaEntity) -> ImobiliariaEntity:
        """
        Salva a entidade. 
        Faz INSERT se o ID for None, caso contrário faz UPDATE.
        """
        with self._get_connection() as conn:
            if entity.id is None:
                cursor = conn.execute("""
                    INSERT INTO imobiliarias (nome, cnpj, contato, observacoes)
                    VALUES (?, ?, ?, ?)
                """, (entity.nome, entity.cnpj, entity.contato, entity.observacoes))
                entity.id = cursor.lastrowid
            else:
                conn.execute("""
                    UPDATE imobiliarias SET 
                        nome = ?, cnpj = ?, contato = ?, observacoes = ?
                    WHERE id = ?
                """, (entity.nome, entity.cnpj, entity.contato, entity.observacoes, entity.id))
        return entity

    def find(self) -> List[ImobiliariaEntity]:
        """Retorna todas as imobiliárias cadastradas."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM imobiliarias")
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]

    def find_by_id(self, imobiliaria_id: int) -> Optional[ImobiliariaEntity]:
        """Busca uma imobiliária pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM imobiliarias WHERE id = ?", (imobiliaria_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_entity(row)
            return None

    def delete(self, imobiliaria_id: int) -> bool:
        """Remove uma imobiliária pelo ID."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM imobiliarias WHERE id = ?", (imobiliaria_id,))
            return cursor.rowcount > 0