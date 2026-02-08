import os
import sys
import subprocess
from datetime import datetime

from src.application.mailing.services.mailing_service import MailingService
from src.infrastructure.mailing.repositories.mailing_repository import MailingRepository
from src.infrastructure.mailing.exporters.mailing_exporter import MailingExporterCompleto
from src.infrastructure.mailing.exporters.mailing_resumido_exporter import MailingExporterResumido


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


# ---------------------------------------------------------
# INGESTÃO GERAL
# ---------------------------------------------------------
def rodar_ingestao():
    print("\nRodando ingestão geral...\n")
    os.system("python -m src.infrastructure.ingestao.ingest")
    input("\nPressione ENTER para voltar ao menu...")


# ---------------------------------------------------------
# EXECUTAR CLI
# ---------------------------------------------------------
def _executar_cli(args):
    comando = ["python", "-m", "src.interface.cli.empreendimento_cli"] + args
    subprocess.run(comando)


# ---------------------------------------------------------
# LISTAR EMPREENDIMENTOS (SEM FILTRO)
# ---------------------------------------------------------
def listar_empreendimentos():
    _executar_cli(["consultar"])
    input("\nPressione ENTER para voltar ao menu...")


# ---------------------------------------------------------
# CONSULTAR COM FILTROS
# ---------------------------------------------------------
def consultar():
    print("\n=== CONSULTA DE EMPREENDIMENTOS ===\n")

    cidade = input("Cidade (ENTER para ignorar): ").strip()
    regiao = input("Região (ENTER para ignorar): ").strip()
    tipologia = input("Tipologia (ENTER para ignorar): ").strip()
    lancamento = input("Lançamento (ENTER para ignorar): ").strip()
    status = input("Status (ENTER para ignorar): ").strip()
    preco_min = input("Preço mínimo (ENTER para ignorar): ").strip()
    preco_max = input("Preço máximo (ENTER para ignorar): ").strip()
    ordenar_por = input("Ordenar por (nome, preco, cidade) (ENTER para ignorar): ").strip()
    ordem = input("Ordem (asc/desc) (ENTER para asc): ").strip() or "asc"

    args = ["consultar"]

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
    if ordenar_por:
        args += ["--ordenar-por", ordenar_por]
    if ordem:
        args += ["--ordem", ordem]

    _executar_cli(args)

    input("\nPressione ENTER para voltar ao menu...")


# ---------------------------------------------------------
# SUBMENU DO MAILING
# ---------------------------------------------------------
def submenu_mailing():
    service = MailingService(MailingRepository())

    while True:
        limpar_tela()
        print("=" * 40)
        print("        MENU DE MAILING")
        print("=" * 40)
        print("1 - Consultar mailing")
        print("2 - Exportar mailing COMPLETO")
        print("3 - Exportar mailing RESUMIDO")
        print("4 - Rodar ingestão de mailing")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_tela()
            print("CONSULTA DE MAILING\n")

            registros = service.consultar()

            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for r in registros:
                    print(f"[{r.id}] {r.nome} - {r.email} - {r.telefone} - {r.origem} - score={r.score_mailing}")
                print(f"\nTotal: {len(registros)} registro(s).")

            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            exporter = MailingExporterCompleto(service)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"mailing_completo_{timestamp}.xlsx"

            pasta = "data/exportacoes/mailing"
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, nome_arquivo)
            exporter.exportar(caminho)

            print(f"\nArquivo exportado como: {nome_arquivo}")
            print(f"Caminho: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            exporter = MailingExporterResumido(service)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"mailing_resumido_{timestamp}.xlsx"

            pasta = "data/exportacoes/mailing"
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, nome_arquivo)
            exporter.exportar(caminho)

            print(f"\nArquivo exportado como: {nome_arquivo}")
            print(f"Caminho: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            os.system("python -m src.infrastructure.ingestao.ingestao_mailing")
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ---------------------------------------------------------
# MENU PRINCIPAL
# ---------------------------------------------------------
def main():
    print(">>> ESTA É A VERSÃO NOVA DO MENU")
    while True:
#        limpar_tela()
        print("=" * 40)
        print("   CORRETOR PLATFORM - MENU")
        print("=" * 40)
        print("1 - Rodar ingestão geral")
        print("2 - Listar empreendimentos")
        print("3 - Consultar empreendimentos")
        print("4 - Mailing")
        print("0 - Sair")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            rodar_ingestao()
        elif opcao == "2":
            listar_empreendimentos()
        elif opcao == "3":
            consultar()
        elif opcao == "4":
            submenu_mailing()
        elif opcao == "0":
            print("\nSaindo...")
            sys.exit()
        else:
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
