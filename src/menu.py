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
# LISTAR EMPREENDIMENTOS
# ---------------------------------------------------------
def listar_empreendimentos():
    _executar_cli(["consultar"])
    input("\nPressione ENTER para voltar ao menu...")


# ---------------------------------------------------------
# CONSULTAR EMPREENDIMENTOS
# ---------------------------------------------------------
def consultar():
    print("\n=== CONSULTA DE EMPREENDIMENTOS ===\n")

    cidade = input("Cidade (ENTER para ignorar): ").strip()
    regiao = input("Região (ENTER para ignorar): ").strip()

    metragem_min = input("Metragem mínima (ENTER para ignorar): ").strip()
    metragem_max = input("Metragem máxima (ENTER para ignorar): ").strip()

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

    if metragem_min != "":
        try:
            args += ["--metragem-min", str(float(metragem_min))]
        except:
            pass

    if metragem_max != "":
        try:
            args += ["--metragem-max", str(float(metragem_max))]
        except:
            pass

    if lancamento:
        args += ["--lancamento", lancamento]
    if status:
        args += ["--status", status]

    if preco_min != "":
        try:
            args += ["--preco-min", str(float(preco_min))]
        except:
            pass

    if preco_max != "":
        try:
            args += ["--preco-max", str(float(preco_max))]
        except:
            pass

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
# SUBMENU DO LEAD
# ---------------------------------------------------------
def submenu_lead():
    from src.application.lead.services.lead_service import LeadService
    from src.infrastructure.lead.repositories.lead_repository import LeadRepository

    service = LeadService(LeadRepository())

    while True:
        limpar_tela()
        print("=" * 40)
        print("        MENU DE LEADS")
        print("=" * 40)
        print("1 - Consultar leads")
        print("2 - Rodar ingestão de leads")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_tela()
            print("CONSULTA DE LEADS\n")

            registros = service.consultar()

            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for r in registros:
                    print(f"[{r.id}] {r.nome} - {r.email} - {r.telefone} - {r.origem} - score={r.score_lead}")
                print(f"\nTotal: {len(registros)} registro(s).")

            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            os.system("python -m src.infrastructure.ingestao.ingestao_lead")
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ---------------------------------------------------------
# SUBMENU DO OFFER ENGINE
# ---------------------------------------------------------
def submenu_offer():
    from src.interface.cli.offer_cli import OfferCLI
    from src.infrastructure.offer.exporters.offer_exporter_completo import OfferExporterCompleto

    cli = OfferCLI()

    exporter = OfferExporterCompleto(
        cli.service,
        cli.lead_repository,
        cli.empreendimento_repository
    )

    while True:
        limpar_tela()
        print("=" * 40)
        print("        MENU DE OFERTAS")
        print("=" * 40)
        print("1 - Gerar ofertas para um lead")
        print("2 - Gerar ofertas para todos os leads")
        print("3 - Listar ofertas de um lead")
        print("4 - Relatório de ofertas para um lead")
        print("5 - Relatório de ofertas para todos os leads")
        print("6 - Exportar ofertas de um lead (XLS)")
        print("7 - Exportar ofertas de TODOS os leads")
        print("8 - Gerar mensagem para WhatsApp")
        print("9 - Matching Engine (Sprint 9)")
        print("0 - Voltar")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_tela()
            cli.generate_for_lead()
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            limpar_tela()
            cli.generate_for_all()
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            limpar_tela()
            cli.list_by_lead()
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            limpar_tela()
            cli.report_for_lead()
            input("\nPressione ENTER para voltar...")

        elif opcao == "5":
            limpar_tela()
            cli.report_for_all()
            input("\nPressione ENTER para voltar...")

        elif opcao == "6":
            limpar_tela()
            lead_id_str = input("ID do lead: ").strip()

            if not lead_id_str.isdigit():
                print("ID inválido.")
                input("\nPressione ENTER para voltar...")
                continue

            lead_id = int(lead_id_str)
            pasta = "data/exportacoes/ofertas"
            os.makedirs(pasta, exist_ok=True)

            caminho = os.path.join(pasta, f"lead_{lead_id}.xlsx")

            try:
                exporter.exportar_por_lead(lead_id, caminho)
                print(f"\nArquivo exportado: {caminho}")
            except Exception as e:
                print(f"\nErro ao exportar: {e}")

            input("\nPressione ENTER para voltar...")

        elif opcao == "7":
            limpar_tela()
            pasta = "data/exportacoes/ofertas"
            os.makedirs(pasta, exist_ok=True)

            try:
                arquivos = exporter.exportar_todos(pasta)
                print(f"\n{len(arquivos)} arquivos gerados em: {pasta}")
            except Exception as e:
                print(f"\nErro ao exportar: {e}")

            input("\nPressione ENTER para voltar...")

        elif opcao == "8":
            limpar_tela()
            lead_id_str = input("ID do lead: ").strip()

            if not lead_id_str.isdigit():
                print("ID inválido.")
                input("\nPressione ENTER para voltar...")
                continue

            lead_id = int(lead_id_str)
            msg = cli.whatsapp_formatter.gerar_mensagem(lead_id)

            print("\n=== MENSAGEM PARA WHATSAPP ===\n")
            print(msg)
            print("\n(Copie e cole no WhatsApp)")
            input("\nPressione ENTER para voltar...")

        # ---------------------------------------------------------
        # AQUI ESTÁ A ÚNICA PARTE AJUSTADA: MATCHING ENGINE
        # ---------------------------------------------------------
        elif opcao == "9":
            limpar_tela()
            print("=" * 40)
            print("        MATCHING ENGINE (Sprint 9)")
            print("=" * 40)
            print("1 - Matching para um lead")
            print("2 - Matching para todos os leads")
            print("3 - Listar matchings de um lead")
            print("4 - Melhores matchings de um lead")
            print("5 - Exportar matching de um lead (XLS)")
            print("6 - Exportar matching de TODOS os leads (XLS)")
            print("7 - Gerar mensagem para WhatsApp")
            print("0 - Voltar")
            print("=" * 40)

            opcao = input("Escolha uma opção: ").strip()

            # 1 - Matching para um lead
            if opcao == "1":
                lead_id = input("\nID do lead: ").strip()
                if lead_id.isdigit():
                    subprocess.run([
                        "python", "-m", "src.interface.cli.matching_cli",
                        "run", "--lead-id", lead_id
                    ])
                input("\nPressione ENTER para voltar...")

            # 2 - Matching para todos os leads
            elif opcao == "2":
                subprocess.run([
                    "python", "-m", "src.interface.cli.matching_cli",
                    "run-all"
                ])
                input("\nPressione ENTER para voltar...")

            # 3 - Listar matchings
            elif opcao == "3":
                lead_id = input("\nID do lead: ").strip()
                if lead_id.isdigit():
                    subprocess.run([
                        "python", "-m", "src.interface.cli.matching_cli",
                        "list", "--lead-id", lead_id
                    ])
                input("\nPressione ENTER para voltar...")

            # 4 - Melhores matchings
            elif opcao == "4":
                lead_id = input("\nID do lead: ").strip()
                limit = input("Limite (padrão 5): ").strip() or "5"
                if lead_id.isdigit():
                    subprocess.run([
                        "python", "-m", "src.interface.cli.matching_cli",
                        "best", "--lead-id", lead_id, "--limit", limit
                    ])
                input("\nPressione ENTER para voltar...")

            # 5 - Exportar matching de um lead
            elif opcao == "5":
                lead_id = input("\nID do lead: ").strip()
                if not lead_id.isdigit():
                    print("ID inválido.")
                    input("\nPressione ENTER para voltar...")
                    continue

                pasta = "data/exportacoes/matching"
                os.makedirs(pasta, exist_ok=True)
                caminho = f"{pasta}/lead_{lead_id}.xlsx"

                subprocess.run([
                    "python", "-m", "src.interface.cli.matching_cli",
                    "export", "--lead-id", lead_id, "--out", caminho
                ])

                print(f"\nArquivo exportado: {caminho}")
                input("\nPressione ENTER para voltar...")

            # 6 - Exportar matching de todos os leads
            elif opcao == "6":
                pasta = "data/exportacoes/matching"
                os.makedirs(pasta, exist_ok=True)

                subprocess.run([
                    "python", "-m", "src.interface.cli.matching_cli",
                    "export-all", "--out", pasta
                ])

                print(f"\nArquivos exportados em: {pasta}")
                input("\nPressione ENTER para voltar...")

            # 7 - Mensagem WhatsApp 
            elif opcao == "7": 
                lead_id = input("\nID do lead: ").strip() 
                if not lead_id.isdigit(): 
                    print("ID inválido.") 
                    input("\nPressione ENTER para voltar...") 
                    continue 
                
                subprocess.run([
                    "python", "-m", "src.interface.cli.matching_cli", 
                    "whatsapp", "--lead-id", lead_id
                ]) 
                
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
        print("=" * 40)
        print("   CORRETOR PLATFORM - MENU")
        print("=" * 40)
        print("1 - Rodar ingestão geral")
        print("2 - Listar empreendimentos")
        print("3 - Consultar empreendimentos")
        print("4 - Mailing")
        print("5 - Lead")
        print("6 - Ofertas")
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
        elif opcao == "5":
            submenu_lead()
        elif opcao == "6":
            submenu_offer()
        elif opcao == "0":
            print("\nSaindo...")
            sys.exit()
        else:
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
