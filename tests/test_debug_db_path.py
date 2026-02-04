import sqlite3

def test_debug_db_path():
    conn = sqlite3.connect("corretor.db")
    cur = conn.cursor()

    print("USANDO BANCO:", conn.execute("PRAGMA database_list").fetchall())

    try:
        cur.execute("SELECT * FROM construtora_imobiliaria LIMIT 1")
        print("TABELA ENCONTRADA!")
    except Exception as e:
        print("ERRO:", e)
