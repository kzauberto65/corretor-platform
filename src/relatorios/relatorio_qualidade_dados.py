# src/relatorios/relatorio_qualidade_dados.py

import sqlite3
from pathlib import Path


# Localização automática do banco corretor.db
def get_db_path():
    root = Path(__file__).resolve().parents[2]
    return root / "database" / "corretor.db"


DB_PATH = get_db_path()


def run_query(conn, query, params=None):
    cur = conn.cursor()
    cur.execute(query, params or [])
    cols = [c[0] for c in cur.description]
    rows = cur.fetchall()
    return cols, rows


def print_section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_table(cols, rows, max_rows=20):
    if not rows:
        print("Nenhum registro encontrado.")
        return

    header = " | ".join(cols)
    print(header)
    print("-" * len(header))

    for row in rows[:max_rows]:
        print(" | ".join(str(v) if v is not None else "" for v in row))

    if len(rows) > max_rows:
        print(f"... ({len(rows) - max_rows} linhas adicionais não exibidas)")


def main():
    if not DB_PATH.exists():
        print(f"Banco de dados não encontrado em: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)

    try:
        # 1. Métricas gerais
        print_section("1. MÉTRICAS GERAIS DA BASE")
        cols, rows = run_query(conn, """
            SELECT 'empreendimentos' AS tabela, COUNT(*) AS total FROM empreendimentos
            UNION ALL
            SELECT 'unidades', COUNT(*) FROM unidades
            UNION ALL
            SELECT 'construtoras', COUNT(*) FROM construtoras
            UNION ALL
            SELECT 'imobiliarias', COUNT(*) FROM imobiliarias
            UNION ALL
            SELECT 'corretores', COUNT(*) FROM corretores
            UNION ALL
            SELECT 'construtora_imobiliaria', COUNT(*) FROM construtora_imobiliaria
            UNION ALL
            SELECT 'corretor_imobiliaria', COUNT(*) FROM corretor_imobiliaria;
        """)
        print_table(cols, rows)

        # 2. Empreendimentos sem unidades
        print_section("2. EMPREENDIMENTOS SEM UNIDADES")
        cols, rows = run_query(conn, """
            SELECT e.id, e.nome, e.cidade, e.estado
            FROM empreendimentos e
            LEFT JOIN unidades u ON u.empreendimento_id = e.id
            WHERE u.id IS NULL;
        """)
        print_table(cols, rows)

        # 3. Empreendimentos duplicados
        print_section("3. EMPREENDIMENTOS DUPLICADOS (nome + cidade)")
        cols, rows = run_query(conn, """
            SELECT nome, cidade, COUNT(*) AS qtd
            FROM empreendimentos
            GROUP BY nome, cidade
            HAVING COUNT(*) > 1;
        """)
        print_table(cols, rows)

        # 4. Datas inválidas
        print_section("4. EMPREENDIMENTOS COM DATAS INVÁLIDAS")
        cols, rows = run_query(conn, """
            SELECT id, nome, data_entrega
            FROM empreendimentos
            WHERE data_entrega IS NOT NULL
              AND data_entrega NOT LIKE '____-__-__%';
        """)
        print_table(cols, rows)

        # 5. Sem cidade/estado
        print_section("5. EMPREENDIMENTOS SEM CIDADE OU ESTADO")
        cols, rows = run_query(conn, """
            SELECT id, nome
            FROM empreendimentos
            WHERE cidade IS NULL OR cidade = ''
               OR estado IS NULL OR estado = '';
        """)
        print_table(cols, rows)

        # 6. Sem tipologia
        print_section("6. EMPREENDIMENTOS SEM TIPOLOGIA")
        cols, rows = run_query(conn, """
            SELECT id, nome
            FROM empreendimentos
            WHERE tipologia IS NULL OR tipologia = '';
        """)
        print_table(cols, rows)

        # 7. Unidades sem empreendimento válido
        print_section("7. UNIDADES SEM EMPREENDIMENTO VÁLIDO")
        cols, rows = run_query(conn, """
            SELECT id, codigo_unidade, empreendimento_id
            FROM unidades
            WHERE empreendimento_id NOT IN (SELECT id FROM empreendimentos);
        """)
        print_table(cols, rows)

        # 8. Unidades com metragem inválida
        print_section("8. UNIDADES COM METRAGEM INVÁLIDA")
        cols, rows = run_query(conn, """
            SELECT id, codigo_unidade, metragem
            FROM unidades
            WHERE metragem IS NULL OR metragem <= 0;
        """)
        print_table(cols, rows)

        # 9. Unidades com valor inválido
        print_section("9. UNIDADES COM VALOR INVÁLIDO")
        cols, rows = run_query(conn, """
            SELECT id, codigo_unidade, valor
            FROM unidades
            WHERE valor IS NULL OR valor <= 0;
        """)
        print_table(cols, rows)

        # 10. Corretores sem imobiliária
        print_section("10. CORRETORES SEM IMOBILIÁRIA")
        cols, rows = run_query(conn, """
            SELECT c.id, c.nome
            FROM corretores c
            LEFT JOIN corretor_imobiliaria ci ON ci.corretor_id = c.id
            WHERE ci.corretor_id IS NULL;
        """)
        print_table(cols, rows)

        # 11. Imobiliárias sem corretores
        print_section("11. IMOBILIÁRIAS SEM CORRETORES")
        cols, rows = run_query(conn, """
            SELECT i.id, i.nome
            FROM imobiliarias i
            LEFT JOIN corretor_imobiliaria ci ON ci.imobiliaria_id = i.id
            WHERE ci.imobiliaria_id IS NULL;
        """)
        print_table(cols, rows)

        # 12. Construtoras sem imobiliárias
        print_section("12. CONSTRUTORAS SEM IMOBILIÁRIAS")
        cols, rows = run_query(conn, """
            SELECT c.id, c.nome
            FROM construtoras c
            LEFT JOIN construtora_imobiliaria ci ON ci.construtora_id = c.id
            WHERE ci.construtora_id IS NULL;
        """)
        print_table(cols, rows)

        # 13. Relacionamentos inválidos CI
        print_section("13. RELACIONAMENTOS INVÁLIDOS: CONSTRUTORA ↔ IMOBILIÁRIA")
        cols, rows = run_query(conn, """
            SELECT *
            FROM construtora_imobiliaria
            WHERE construtora_id NOT IN (SELECT id FROM construtoras)
               OR imobiliaria_id NOT IN (SELECT id FROM imobiliarias);
        """)
        print_table(cols, rows)

        # 14. Relacionamentos inválidos Corretor-Imobiliária
        print_section("14. RELACIONAMENTOS INVÁLIDOS: CORRETOR ↔ IMOBILIÁRIA")
        cols, rows = run_query(conn, """
            SELECT *
            FROM corretor_imobiliaria
            WHERE corretor_id NOT IN (SELECT id FROM corretores)
               OR imobiliaria_id NOT IN (SELECT id FROM imobiliarias);
        """)
        print_table(cols, rows)

        # 15. Dashboard consolidado
        print_section("15. DASHBOARD CONSOLIDADO")
        cols, rows = run_query(conn, """
            SELECT
                (SELECT COUNT(*) FROM empreendimentos) AS total_empreendimentos,
                (SELECT COUNT(*) FROM unidades) AS total_unidades,
                (SELECT COUNT(*) FROM corretores) AS total_corretores,
                (SELECT COUNT(*) FROM imobiliarias) AS total_imobiliarias,
                (SELECT COUNT(*) FROM construtoras) AS total_construtoras,
                (SELECT COUNT(*) FROM unidades WHERE valor <= 0 OR valor IS NULL) AS unidades_valor_invalido,
                (SELECT COUNT(*) FROM unidades WHERE metragem <= 0 OR metragem IS NULL) AS unidades_metragem_invalida,
                (SELECT COUNT(*) FROM empreendimentos WHERE cidade IS NULL OR cidade = '') AS empreendimentos_sem_cidade,
                (SELECT COUNT(*) FROM empreendimentos WHERE tipologia IS NULL OR tipologia = '') AS empreendimentos_sem_tipologia,
                (SELECT COUNT(*) FROM corretores c LEFT JOIN corretor_imobiliaria ci ON ci.corretor_id = c.id WHERE ci.corretor_id IS NULL) AS corretores_sem_imobiliaria;
        """)
        print_table(cols, rows, max_rows=5)

    finally:
        conn.close()


if __name__ == "__main__":
    main()