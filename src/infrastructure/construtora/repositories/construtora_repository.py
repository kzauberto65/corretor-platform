# ============================================================
# REPOSITORY: ConstrutoraRepository
# Camada: infrastructure/construtora/repositories/
# Descrição: Acesso a dados para Construtoras.
#            Responsável por interagir com o banco de dados SQLite.
#            Mapeia objetos `ConstrutoraEntity` para tabelas SQL.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================
# ====

import sqlite3
from typing import Optional, List
from src.domain.construtora.entities.construtora_entity import ConstrutoraEntity


class ConstrutoraRepository:
    # Mapeamento dos nomes das colunas da tabela para os atributos da Entity
    _COLUMNS = (
        "id", "nome", "cnpj", "contato", "observacoes",
        "fonte", "data_registro", "usuario_id", "justificativa"
    )

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        # Permite acessar colunas por nome (Ex: row['nome'])
        conn.row_factory = sqlite3.Row
        # Habilita chaves estrangeiras no SQLite
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _row_to_entity(self, row: sqlite3.Row) -> ConstrutoraEntity:
        """Converte uma linha do SQLite em um objeto ConstrutoraEntity."""
        return ConstrutoraEntity(
            id=row["id"],
            nome=row["nome"],
            cnpj=row["cnpj"],
            contato=row["contato"],
            observacoes=row["observacoes"],
            fonte=row["fonte"],
            data_registro=row["data_registro"],
            usuario_id=row["usuario_id"],
            justificativa=row["justificativa"]
        )

    def save(self, entity: ConstrutoraEntity) -> ConstrutoraEntity:
        """Salva uma nova Construtora no banco de dados ou atualiza uma existente."""
        with self._conn() as conn:
            cur = conn.cursor()
            if entity.id is None:  # INSERT (novo registro)
                columns = ", ".join(self._COLUMNS[1:])  # Exclui 'id' do insert
                placeholders = ", ".join(["?"] * (len(self._COLUMNS) - 1))
                query = f"""
                    INSERT INTO construtoras
                    ({columns})
                    VALUES ({placeholders})
                """
                cur.execute(query, (
                    entity.nome, entity.cnpj, entity.contato, entity.observacoes,
                    entity.fonte, entity.data_registro, entity.usuario_id, entity.justificativa
                ))
                entity.id = cur.lastrowid
            else:  # UPDATE (registro existente)
                query = """
                    UPDATE construtoras SET
                        nome = ?, cnpj = ?, contato = ?, observacoes = ?, fonte = ?,
                        data_registro = ?, usuario_id = ?, justificativa = ?
                    WHERE id = ?
                """
                cur.execute(query, (
                    entity.nome, entity.cnpj, entity.contato, entity.observacoes,
                    entity.fonte, entity.data_registro, entity.usuario_id,
                    entity.justificativa, entity.id
                ))
        return entity

    def update(self, entity: ConstrutoraEntity) -> ConstrutoraEntity:
        return self.save(entity)

    def find(self) -> List[ConstrutoraEntity]:
        """Busca todas as construtoras no banco de dados."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM construtoras")
            rows = cur.fetchall()
        return [self._row_to_entity(r) for r in rows]

    def find_by_id(self, id: int) -> Optional[ConstrutoraEntity]:
        """Busca uma construtora pelo seu ID."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM construtoras WHERE id = ?", (id,))
            row = cur.fetchone()
        if row:
            return self._row_to_entity(row)
        return None

    def delete(self, id: int) -> bool:
        """Remove uma construtora do banco de dados pelo seu ID."""
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM construtoras WHERE id = ?", (id,))
            return cur.rowcount > 0