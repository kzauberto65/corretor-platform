import sqlite3
import json
from src.domain.matching.entities.matching_entity import MatchingEntity


class MatchingRepository:

    def __init__(self, db_path="src/infrastructure/database/corretor.db"):
        self.db_path = db_path

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def save(self, entity: MatchingEntity) -> int:
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO matching (
                lead_id,
                property_id,
                score,
                reasons_json,
                created_at
            )
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (
            entity.lead_id,
            entity.property_id,
            entity.score,
            json.dumps(entity.reasons_json)
        ))

        conn.commit()
        last_id = cur.lastrowid
        conn.close()
        return last_id

    def list_by_lead(self, lead_id: int):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, lead_id, property_id, score, reasons_json, created_at
            FROM matching
            WHERE lead_id = ?
            ORDER BY score DESC
        """, (lead_id,))

        rows = cur.fetchall()
        conn.close()

        return [
            MatchingEntity(
                id=row[0],
                lead_id=row[1],
                property_id=row[2],
                score=row[3],
                reasons_json=json.loads(row[4]),
                created_at=row[5]
            )
            for row in rows
        ]

    def list_best_matches(self, lead_id: int, limit: int = 5):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, lead_id, property_id, score, reasons_json, created_at
            FROM matching
            WHERE lead_id = ?
            ORDER BY score DESC
            LIMIT ?
        """, (lead_id, limit))

        rows = cur.fetchall()
        conn.close()

        return [
            MatchingEntity(
                id=row[0],
                lead_id=row[1],
                property_id=row[2],
                score=row[3],
                reasons_json=json.loads(row[4]),
                created_at=row[5]
            )
            for row in rows
        ]
