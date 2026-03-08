import sqlite3
import json
from src.domain.ia.entities.ia_entity import IAEntity


class IARepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    def save(self, entity: IAEntity) -> int:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO ia_score (
                lead_id,
                property_id,
                similarity,
                conversion_score,
                lead_vector,
                property_vector,
                reasons_json,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entity.lead_id,
            entity.property_id,
            entity.similarity,
            entity.conversion_score,
            json.dumps(entity.lead_vector),
            json.dumps(entity.property_vector),
            json.dumps(entity.reasons_json),
            entity.created_at
        ))

        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    # ---------------------------------------------------------
    # LIST BY LEAD
    # ---------------------------------------------------------
    def list_by_lead(self, lead_id: int):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                lead_id,
                property_id,
                similarity,
                conversion_score,
                lead_vector,
                property_vector,
                reasons_json,
                created_at
            FROM ia_score
            WHERE lead_id = ?
            ORDER BY similarity DESC
        """, (lead_id,))

        rows = cur.fetchall()
        conn.close()

        return [
            IAEntity(
                id=row[0],
                lead_id=row[1],
                property_id=row[2],
                similarity=row[3],
                conversion_score=row[4],
                lead_vector=json.loads(row[5]),
                property_vector=json.loads(row[6]),
                reasons_json=json.loads(row[7]),
                created_at=row[8]
            )
            for row in rows
        ]

    # ---------------------------------------------------------
    # LIST BEST RESULTS
    # ---------------------------------------------------------
    def list_best(self, lead_id: int, limit: int = 5):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                lead_id,
                property_id,
                similarity,
                conversion_score,
                lead_vector,
                property_vector,
                reasons_json,
                created_at
            FROM ia_score
            WHERE lead_id = ?
            ORDER BY conversion_score DESC
            LIMIT ?
        """, (lead_id, limit))

        rows = cur.fetchall()
        conn.close()

        return [
            IAEntity(
                id=row[0],
                lead_id=row[1],
                property_id=row[2],
                similarity=row[3],
                conversion_score=row[4],
                lead_vector=json.loads(row[5]),
                property_vector=json.loads(row[6]),
                reasons_json=json.loads(row[7]),
                created_at=row[8]
            )
            for row in rows
        ]

    # ---------------------------------------------------------
    # NOVO: LISTAR TODOS OS REGISTROS
    # ---------------------------------------------------------
    def list_all(self):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                id,
                lead_id,
                property_id,
                similarity,
                conversion_score,
                lead_vector,
                property_vector,
                reasons_json,
                created_at
            FROM ia_score
            ORDER BY lead_id ASC, conversion_score DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            IAEntity(
                id=row[0],
                lead_id=row[1],
                property_id=row[2],
                similarity=row[3],
                conversion_score=row[4],
                lead_vector=json.loads(row[5]),
                property_vector=json.loads(row[6]),
                reasons_json=json.loads(row[7]),
                created_at=row[8]
            )
            for row in rows
        ]

    # ---------------------------------------------------------
    # NOVO: AGRUPAR POR LEAD
    # ---------------------------------------------------------
    def list_grouped_by_lead(self):
        all_scores = self.list_all()
        grouped = {}

        for score in all_scores:
            if score.lead_id not in grouped:
                grouped[score.lead_id] = []
            grouped[score.lead_id].append(score)

        return grouped
