import sqlite3
from src.domain.construtora_imobiliaria.entities.construtora_imobiliaria_entity import ConstrutoraImobiliariaEntity
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_dto import ConstrutoraImobiliariaDTO

class ConstrutoraImobiliariaRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def cadastrar(self, entity: ConstrutoraImobiliariaEntity) -> ConstrutoraImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO construtora_imobiliaria (
                construtora_id,
                imobiliaria_id,
                tipo_parceria,
                observacoes
            )
            VALUES (?, ?, ?, ?)
        """, (
            entity.construtora_id,
            entity.imobiliaria_id,
            entity.tipo_parceria,
            entity.observacoes
        ))

        conn.commit()
        conn.close()
        return entity

    def atualizar(self, entity: ConstrutoraImobiliariaEntity) -> ConstrutoraImobiliariaEntity:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE construtora_imobiliaria
            SET tipo_parceria = ?, observacoes = ?
            WHERE construtora_id = ? AND imobiliaria_id = ?
        """, (
            entity.tipo_parceria,
            entity.observacoes,
            entity.construtora_id,
            entity.imobiliaria_id
        ))

        conn.commit()
        conn.close()
        return entity

    def consultar(self) -> list[ConstrutoraImobiliariaDTO]:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT construtora_id, imobiliaria_id, tipo_parceria, observacoes
            FROM construtora_imobiliaria
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            ConstrutoraImobiliariaDTO(
                construtora_id=row[0],
                imobiliaria_id=row[1],
                tipo_parceria=row[2],
                observacoes=row[3]
            )
            for row in rows
        ]

    def buscar_por_ids(self, construtora_id: int, imobiliaria_id: int) -> ConstrutoraImobiliariaDTO | None:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT construtora_id, imobiliaria_id, tipo_parceria, observacoes
            FROM construtora_imobiliaria
            WHERE construtora_id = ? AND imobiliaria_id = ?
        """, (construtora_id, imobiliaria_id))

        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return ConstrutoraImobiliariaDTO(
            construtora_id=row[0],
            imobiliaria_id=row[1],
            tipo_parceria=row[2],
            observacoes=row[3]
        )

    def remover(self, construtora_id: int, imobiliaria_id: int) -> bool:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM construtora_imobiliaria
            WHERE construtora_id = ? AND imobiliaria_id = ?
        """, (construtora_id, imobiliaria_id))

        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()

        return deleted
