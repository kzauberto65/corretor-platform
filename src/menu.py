import os
import sys


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def rodar_ingestao():
    print("\nRodando ingestão...\n")
    os.system("python src/ingestao/ingest.py")
    input("\nPressione ENTER para voltar ao menu...")


def listar_empreendimentos():
    os.system("python -m src.cli.empreendimentos_cli --listar")
    input("\nPressione ENTER para voltar ao menu...")


def consultar():
    cidade = input("Cidade (ENTER para ignorar): ").strip()
    regiao = input("Região (ENTER para ignorar): ").strip()
    tipologia = input("Tipologia (ENTER para ignorar): ").strip()
    lancamento = input("Lançamento (ENTER para ignorar): ").strip()
    status = input("Status (ENTER para ignorar): ").strip()
    preco_max = input("Preço máximo (ENTER para ignorar): ").strip()

    comando = "python -m src.cli.empreendimentos_cli"

    if cidade:
        comando += f' --cidade "{cidade}"'
    if regiao:
        comando += f' --regiao "{regiao}"'
    if tipologia:
        comando += f' --tipologia "{tipologia}"'
    if lancamento:
        comando += f' --lancamento "{lancamento}"'
    if status:
        comando += f' --status "{status}"'
    if preco_max:
        comando += f' --preco-max {preco_max}'

    print("\nExecutando consulta...\n")
    os.system(comando)
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
            input("Pressione ENTER para tentar novamente...")


if __name__ == "__main__":
    main()
