import sqlite3
from pathlib import Path
from src.parsing import get_project_root

ROOT = get_project_root()
DB_PATH = ROOT / "database" / "corretor.db"
SCHEMA_PATH = ROOT / "database" / "schema.sql"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema = f.read()

        try:
            conn.executescript(schema)
            print(f"Banco inicializado em: {DB_PATH}")
        except sqlite3.Error as e:
            print("Erro ao aplicar schema.sql:")
            print(e)

if __name__ == "__main__":
    init_db()