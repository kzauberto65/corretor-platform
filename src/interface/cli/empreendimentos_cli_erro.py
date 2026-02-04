import argparse

from src.application.buscar_empreendimentos import BuscarEmpreendimentos
from src.servicos.query_service import QueryService


def imprimir_tabela(empreendimentos):
    if not empreendimentos:
        print("Nenhum resultado encontrado.")
        return

    for e in empreendimentos:
        print(e)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--listar", action="store_true")

    parser.add_argument("--cidade")
    parser.add_argument("--regiao")
    parser.add_argument("--tipologia")
    parser.add_argument("--lancamento")
    parser.add_argument("--status")
    parser.add_argument("--preco-min", type=float)
    parser.add_argument("--preco-max", type=float)
    parser.add_argument("--pagina", type=int, default=1)
    parser.add_argument("--por-pagina", type=int, default=10)
    parser.add_argument("--ordenar-por")
    parser.add_argument("--ordem", default="asc")

    args = parser.parse_args()

    if not args.listar:
        return

    filtros = {
        "cidade": args.cidade,
        "regiao": args.regiao,
        "tipologia": args.tipologia,
        "lancamento": args.lancamento,
        "status": args.status,
        "preco_min": args.preco_min,
        "preco_max": args.preco_max,
    }

    use_case = BuscarEmpreendimentos(QueryService())

    resultado = use_case.executar(
        filtros=filtros,
        pagina=args.pagina,
        por_pagina=args.por_pagina,
        ordenar_por=args.ordenar_por,
        ordem=args.ordem
    )

    imprimir_tabela(resultado["dados"])
    print(f"\nPágina {resultado['pagina']} de {resultado['total_paginas']}")


if __name__ == "__main__":
    main()
