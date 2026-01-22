import argparse

from src.servicos.empreendimento_service import EmpreendimentoService
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
            e["nome"][:26],
            e["regiao"] or "",
            e["cidade"] or "",
            e["bairro"] or "",
            e["tipologia"] or "",
            e["periodo_lancamento"] or "",
            e["status_entrega"] or "",
            f'{e["preco"]:.0f}' if e["preco"] else ""
        ))


def listar():
    service = EmpreendimentoService()
    empreendimentos = service.listar_empreendimentos()
    imprimir_tabela(empreendimentos)


def buscar_por_id(empreendimento_id):
    service = EmpreendimentoService()
    emp = service.buscar_por_id(empreendimento_id)

    if not emp:
        print("Empreendimento não encontrado.")
        return

    imprimir_tabela([emp])


def main():
    parser = argparse.ArgumentParser(description="CLI de consulta de empreendimentos")

    parser.add_argument("--listar", action="store_true", help="Listar todos os empreendimentos")
    parser.add_argument("--id", type=int, help="Buscar empreendimento por ID")

    parser.add_argument("--cidade", type=str, help="Filtrar por cidade")
    parser.add_argument("--regiao", type=str, help="Filtrar por região")
    parser.add_argument("--tipologia", type=str, help="Filtrar por tipologia")
    parser.add_argument("--lancamento", type=str, help="Filtrar por período de lançamento")
    parser.add_argument("--status", type=str, help="Filtrar por status de entrega")
    parser.add_argument("--preco-min", type=float, help="Preço mínimo")
    parser.add_argument("--preco-max", type=float, help="Preço máximo")
    args = parser.parse_args()

    if args.listar:
        listar()
        return

    if args.id:
        buscar_por_id(args.id)
        return

    if (
        args.cidade or args.regiao or args.tipologia or
        args.lancamento or args.status or
        args.preco_min or args.preco_max
    ):
        qs = QueryService()
        resultados = qs.buscar_empreendimentos(
            cidade=args.cidade,
            regiao=args.regiao,
            tipologia=args.tipologia,
            periodo_lancamento=args.lancamento,
            status=args.status,
            preco_min=args.preco_min,
            preco_max=args.preco_max
        )
        imprimir_tabela(resultados)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
