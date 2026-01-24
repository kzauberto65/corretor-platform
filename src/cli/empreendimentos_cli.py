import argparse
import os
import csv
from datetime import datetime
from openpyxl import Workbook

from src.application.buscar_empreendimentos import BuscarEmpreendimentos
from src.servicos.query_service import QueryService


def imprimir_tabela(empreendimentos):
    if not empreendimentos:
        print("Nenhum resultado encontrado.")
        return

    headers = [
        "ID", "Nome", "Região", "Cidade", "Bairro",
        "Tipologia", "Lançamento", "Status", "Preço"
    ]

    print("{:<4} {:<28} {:<12} {:<15} {:<15} {:<18} {:<15} {:<15} {:>10}".format(*headers))
    print("-" * 150)

    for e in empreendimentos:
        print("{:<4} {:<28} {:<12} {:<15} {:<15} {:<18} {:<15} {:<15} {:>10}".format(
            e["id"],
            (e["nome"] or "")[:26],
            e["regiao"] or "",
            e["cidade"] or "",
            e["bairro"] or "",
            e["tipologia"] or "",
            e["periodo_lancamento"] or "",
            e["status_entrega"] or "",
            f'{e["preco"]:.0f}' if e["preco"] else ""
        ))


def escolher_ordenacao():
    print("\nOrdenação (opcional):")
    print("1 - Preço")
    print("2 - Cidade")
    print("3 - Nome")
    print("4 - Lançamento")
    print("5 - Região")
    print("ENTER - Sem ordenação")

    escolha = input("Escolha: ").strip()

    if escolha == "":
        return None  # ENTER = sem ordenação

    mapa = {
        "1": "preco",
        "2": "cidade",
        "3": "nome",
        "4": "lancamento",
        "5": "regiao"
    }

    return mapa.get(escolha)


def exportar_xlsx(todos):
    # Caminho absoluto para /data/exports/
    base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "data", "exports")
    base_dir = os.path.abspath(base_dir)

    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = os.path.join(base_dir, f"consulta_completa_{timestamp}.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "Empreendimentos"

    ws.append([
        "ID", "Nome", "Região", "Cidade", "Bairro",
        "Tipologia", "Lançamento", "Status", "Preço"
    ])

    for e in todos:
        ws.append([
            e["id"],
            e["nome"],
            e["regiao"],
            e["cidade"],
            e["bairro"],
            e["tipologia"],
            e["periodo_lancamento"],
            e["status_entrega"],
            e["preco"]
        ])

    wb.save(caminho)
    print(f"\nArquivo XLSX gerado com sucesso em:\n{caminho}")


def main():
    parser = argparse.ArgumentParser(description="CLI de consulta de empreendimentos")

    parser.add_argument("--listar", action="store_true")

    parser.add_argument("--cidade")
    parser.add_argument("--regiao")
    parser.add_argument("--tipologia")
    parser.add_argument("--lancamento")
    parser.add_argument("--status")
    parser.add_argument("--preco-min", type=float)
    parser.add_argument("--preco-max", type=float)

    parser.add_argument("--pagina", type=int, default=1)
    parser.add_argument("--por-pagina", type=int, default=3)

    parser.add_argument("--ordenar-por")
    parser.add_argument("--ordem", choices=["asc", "desc"], default="asc")

    args = parser.parse_args()

    filtros = {
        "cidade": args.cidade,
        "regiao": args.regiao,
        "tipologia": args.tipologia,
        "lancamento": args.lancamento,
        "status": args.status,
        "preco_min": args.preco_min,
        "preco_max": args.preco_max,
    }

    # Se o menu enviou --ordenar-por (mesmo vazio), NÃO perguntar de novo
    if args.ordenar_por is not None:
        ordenar_por = args.ordenar_por or None
    else:
        ordenar_por = escolher_ordenacao()

    use_case = BuscarEmpreendimentos(QueryService())
    pagina = args.pagina

    while True:
        print("\nExecutando consulta...\n")

        resultado = use_case.executar(
            filtros=filtros,
            pagina=pagina,
            por_pagina=args.por_pagina,
            ordenar_por=ordenar_por,
            ordem=args.ordem
        )

        imprimir_tabela(resultado["dados"])
        print(f"\nPágina {resultado['pagina']} de {resultado['total_paginas']}")

        # Exportação XLSX de TODOS os resultados
        exportar = input("\nExportar TODOS os resultados para XLSX? (s/N): ").strip().lower()

        if exportar == "s":
            print("\nGerando XLSX com todos os resultados...")

            resultado_completo = use_case.executar(
                filtros=filtros,
                pagina=1,
                por_pagina=999999,  # pega tudo
                ordenar_por=ordenar_por,
                ordem=args.ordem
            )

            exportar_xlsx(resultado_completo["dados"])

        comando = input("\n[N] próxima | [P] anterior | ENTER sair: ").lower()

        if comando == "n" and pagina < resultado["total_paginas"]:
            pagina += 1
        elif comando == "p" and pagina > 1:
            pagina -= 1
        else:
            break


if __name__ == "__main__":
    main()
