import sqlite3
from src.domain.corretor_imobiliaria.entities.corretor_imobiliaria_entity import CorretorImobiliariaEntity
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_dto import CorretorImobiliariaDTO

class CorretorImobiliariaRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: CorretorImobiliariaEntity) -> CorretorImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO corretor_imobiliaria (
                corretor_id,
                imobiliaria_id,
                tipo_vinculo,
                observacoes
            )
            VALUES (?, ?, ?, ?)
        """, (
            entity.corretor_id,
            entity.imobiliaria_id,
            entity.tipo_vinculo,
            entity.observacoes
        ))

        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: CorretorImobiliariaEntity) -> CorretorImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE corretor_imobiliaria
            SET tipo_vinculo = ?, observacoes = ?
            WHERE corretor_id = ? AND imobiliaria_id = ?
        """, (
            entity.tipo_vinculo,
            entity.observacoes,
            entity.corretor_id,
            entity.imobiliaria_id
        ))

        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[CorretorImobiliariaDTO]:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT corretor_id, imobiliaria_id, tipo_vinculo, observacoes
            FROM corretor_imobiliaria
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            CorretorImobiliariaDTO(
                corretor_id=row[0],
                imobiliaria_id=row[1],
                tipo_vinculo=row[2],
                observacoes=row[3]
            )
            for row in rows
        ]

    def buscar_por_ids(self, corretor_id: int, imobiliaria_id: int) -> CorretorImobiliariaDTO | None:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT corretor_id, imobiliaria_id, tipo_vinculo, observacoes
            FROM corretor_imobiliaria
            WHERE corretor_id = ? AND imobiliaria_id = ?
        """, (corretor_id, imobiliaria_id))

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return CorretorImobiliariaDTO(
            corretor_id=row[0],
            imobiliaria_id=row[1],
            tipo_vinculo=row[2],
            observacoes=row[3]
        )

    def remover(self, corretor_id: int, imobiliaria_id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM corretor_imobiliaria
            WHERE corretor_id = ? AND imobiliaria_id = ?
        """, (corretor_id, imobiliaria_id))

        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()

        return deleted
