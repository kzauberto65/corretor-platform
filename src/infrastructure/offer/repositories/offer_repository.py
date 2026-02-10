import sqlite3
from src.domain.offer.dto.offer_normalized_dto import OfferNormalizedDTO
from src.domain.offer.entities.offer_entity import OfferEntity


class OfferRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # SALVAR
    # ---------------------------------------------------------
    def save(self, dto: OfferNormalizedDTO):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO offer (
                lead_id,
                empreendimento_id,
                score,
                rationale
            )
            VALUES (?, ?, ?, ?)
        """, (
            dto.lead_id,
            dto.empreendimento_id,
            dto.score,
            dto.rationale
        ))

        conn.commit()
        conn.close()

    # ---------------------------------------------------------
    # BUSCAR POR LEAD
    # ---------------------------------------------------------
    def find_by_lead(self, lead_id: int):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                lead_id,
                empreendimento_id,
                score,
                rationale,
                created_at
            FROM offer
            WHERE lead_id = ?
            ORDER BY score DESC
        """, (lead_id,))

        rows = cur.fetchall()
        conn.close()

        resultados = []
        for row in rows:
            resultados.append(OfferEntity(
                id=row[0],
                lead_id=row[1],
                empreendimento_id=row[2],
                score=row[3],
                rationale=row[4],
                created_at=row[5]
            ))

        return resultados

    # ---------------------------------------------------------
    # LISTAR TODAS
    # ---------------------------------------------------------
    def find_all(self):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                lead_id,
                empreendimento_id,
                score,
                rationale,
                created_at
            FROM offer
            ORDER BY created_at DESC
        """)

        rows = cur.fetchall()
        conn.close()

        resultados = []
        for row in rows:
            resultados.append(OfferEntity(
                id=row[0],
                lead_id=row[1],
                empreendimento_id=row[2],
                score=row[3],
                rationale=row[4],
                created_at=row[5]
            ))

        return resultados
