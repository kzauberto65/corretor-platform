import sqlite3
from src.domain.corretor_unidade.entities.corretor_unidade_entity import CorretorUnidadeEntity
from src.domain.corretor_unidade.dto.corretor_unidade_dto import CorretorUnidadeDTO

class CorretorUnidadeRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: CorretorUnidadeEntity) -> CorretorUnidadeEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO corretor_unidade (
                corretor_id,
                unidade_id,
                tipo_vinculo,
                observacoes
            )
            VALUES (?, ?, ?, ?)
        """, (
            entity.corretor_id,
            entity.unidade_id,
            entity.tipo_vinculo,
            entity.observacoes
        ))

        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: CorretorUnidadeEntity) -> CorretorUnidadeEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE corretor_unidade
            SET tipo_vinculo = ?, observacoes = ?
            WHERE corretor_id = ? AND unidade_id = ?
        """, (
            entity.tipo_vinculo,
            entity.observacoes,
            entity.corretor_id,
            entity.unidade_id
        ))

        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[CorretorUnidadeDTO]:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT corretor_id, unidade_id, tipo_vinculo, observacoes
            FROM corretor_unidade
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            CorretorUnidadeDTO(
                corretor_id=row[0],
                unidade_id=row[1],
                tipo_vinculo=row[2],
                observacoes=row[3]
            )
            for row in rows
        ]

    def buscar_por_ids(self, corretor_id: int, unidade_id: int) -> CorretorUnidadeDTO | None:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT corretor_id, unidade_id, tipo_vinculo, observacoes
            FROM corretor_unidade
            WHERE corretor_id = ? AND unidade_id = ?
        """, (corretor_id, unidade_id))

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return CorretorUnidadeDTO(
            corretor_id=row[0],
            unidade_id=row[1],
            tipo_vinculo=row[2],
            observacoes=row[3]
        )

    def remover(self, corretor_id: int, unidade_id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM corretor_unidade
            WHERE corretor_id = ? AND unidade_id = ?
        """, (corretor_id, unidade_id))

        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()

        return deleted
