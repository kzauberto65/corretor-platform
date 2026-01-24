import os
import sys
import subprocess


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def rodar_ingestao():
    print("\nRodando ingestão...\n")
    os.system("python src/ingestao/ingest.py")
    input("\nPressione ENTER para voltar ao menu...")


def listar_empreendimentos():
    subprocess.run(["python", "-m", "src.cli.empreendimentos_cli", "--listar"])
    input("\nPressione ENTER para voltar ao menu...")


def _executar_cli(args):
    comando = ["python", "-m", "src.cli.empreendimentos_cli"] + args
    subprocess.run(comando)


def consultar():
    cidade = input("Cidade (ENTER para ignorar): ").strip()
    regiao = input("Região (ENTER para ignorar): ").strip()
    tipologia = input("Tipologia (ENTER para ignorar): ").strip()
    lancamento = input("Lançamento (ENTER para ignorar): ").strip()
    status = input("Status (ENTER para ignorar): ").strip()
    preco_min = input("Preço mínimo (ENTER para ignorar): ").strip()
    preco_max = input("Preço máximo (ENTER para ignorar): ").strip()

    por_pagina_in = input("Resultados por página (ENTER = 3): ").strip()
    por_pagina = int(por_pagina_in) if por_pagina_in.isdigit() else 3

    print("\nOrdenação (opcional):")
    print("1 - Preço")
    print("2 - Cidade")
    print("3 - Nome")
    print("4 - Lançamento")
    print("5 - Região")
    print("ENTER - Sem ordenação")
    ordenacao_opcao = input("Escolha: ").strip()

    ordenar_por_map = {
        "1": "preco",
        "2": "cidade",
        "3": "nome",
        "4": "lancamento",
        "5": "regiao",
    }

    ordenar_por = ordenar_por_map.get(ordenacao_opcao, "")

    ordem = "asc"
    if ordenar_por:
        ordem_in = input("Ordem (asc/desc) [asc]: ").strip().lower()
        if ordem_in in ("asc", "desc"):
            ordem = ordem_in

    args = []

    if cidade:
        args += ["--cidade", cidade]
    if regiao:
        args += ["--regiao", regiao]
    if tipologia:
        args += ["--tipologia", tipologia]
    if lancamento:
        args += ["--lancamento", lancamento]
    if status:
        args += ["--status", status]
    if preco_min:
        args += ["--preco-min", preco_min]
    if preco_max:
        args += ["--preco-max", preco_max]

    # Sempre envia ordenar-por (mesmo vazio)
    args += ["--ordenar-por", ordenar_por, "--ordem", ordem]

    args += ["--listar", "--pagina", "1", "--por-pagina", str(por_pagina)]

    # Não limpar a tela aqui — isso apagava o CLI
    _executar_cli(args)

    input("\nPressione ENTER para voltar ao menu...")


def main():
    while True:
        limpar_tela()
        print("=" * 40)
        print("   CORRETOR PLATFORM - MENU")
        print("=" * 40)
        print("1 - Rodar ingestão")
        print("2 - Listar empreendimentos")
        print("3 - Consultar empreendimentos")
        print("0 - Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            rodar_ingestao()
        elif opcao == "2":
            listar_empreendimentos()
        elif opcao == "3":
            consultar()
        elif opcao == "0":
            print("\nSaindo...")
            sys.exit()
        else:
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
