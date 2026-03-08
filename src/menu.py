# ============================================================
# MENU: menu.py
# Camada: interface/
# Descrição: Menu principal da plataforma Corretor.
#            Ponto de entrada via menu.bat.
#            Chama CLIs via subprocess — nunca acessa banco diretamente.
# Sprint: 10.5 — filtros de preco/metragem removidos de empreendimentos,
#            submenu de unidades adicionado, ingestão central integrada.
# ============================================================

import os
import sys
import subprocess
from datetime import datetime

from src.application.mailing.services.mailing_service import MailingService
from src.infrastructure.mailing.repositories.mailing_repository import MailingRepository
from src.infrastructure.mailing.exporters.mailing_exporter import MailingExporterCompleto
from src.infrastructure.mailing.exporters.mailing_resumido_exporter import MailingExporterResumido

# Caminho padrão do banco — usado em todos os services instanciados aqui
DB_PATH = "src/infrastructure/database/corretor.db"


def limpar_tela():
    """Limpa o terminal — compatível com Windows e Unix."""
    os.system("cls" if os.name == "nt" else "clear")


def cabecalho(titulo: str):
    """Exibe cabeçalho padronizado para submenus."""
    limpar_tela()
    print("=" * 45)
    print(f"  {titulo}")
    print("=" * 45)


# ----------------------------------------------------------
# INGESTÃO
# ----------------------------------------------------------

def submenu_ingestao():
    """Submenu de ingestão de dados."""
    while True:
        cabecalho("INGESTÃO DE DADOS")
        print("1 - Ingestão CENTRAL (planilha mestre)")
        print("2 - Ingestão de Empreendimentos")
        print("3 - Ingestão de Unidades")
        print("4 - Ingestão de Mailing")
        print("5 - Ingestão de Leads")
        print("6 - Ingestão de Corretores")
        print("7 - Ingestão de Construtoras")
        print("8 - Ingestão de Imobiliárias")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            print("\nIngestão central processa planilha mestre com todas as entidades.")
            arquivo = input("Caminho do arquivo XLSX (ENTER para pasta padrão): ").strip()
            if arquivo:
                os.system(f'python -m src.infrastructure.ingestao.ingestao_central "{arquivo}"')
            else:
                os.system("python -m src.infrastructure.ingestao.ingest")
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            os.system("python -m src.infrastructure.ingestao.ingestao_empreendimento")
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            os.system("python -m src.infrastructure.ingestao.ingestao_unidade")
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            os.system("python -m src.infrastructure.ingestao.ingestao_mailing")
            input("\nPressione ENTER para voltar...")

        elif opcao == "5":
            os.system("python -m src.infrastructure.ingestao.ingestao_lead")
            input("\nPressione ENTER para voltar...")

        elif opcao == "6":
            os.system("python -m src.infrastructure.ingestao.ingestao_corretor")
            input("\nPressione ENTER para voltar...")

        elif opcao == "7":
            os.system("python -m src.infrastructure.ingestao.ingestao_construtora")
            input("\nPressione ENTER para voltar...")

        elif opcao == "8":
            os.system("python -m src.infrastructure.ingestao.ingestao_imobiliaria")
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# EMPREENDIMENTOS
# ----------------------------------------------------------

def _cli_empreendimento(args: list):
    """Executa comando da CLI de empreendimentos."""
    subprocess.run(["python", "-m", "src.interface.cli.empreendimento_cli"] + args)


def submenu_empreendimento():
    """Submenu de gerenciamento de empreendimentos."""
    while True:
        cabecalho("EMPREENDIMENTOS")
        print("1 - Listar todos")
        print("2 - Consultar com filtros")
        print("3 - Buscar por ID")
        print("4 - Listar com unidades disponíveis")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            _cli_empreendimento(["consultar"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            print("\n=== FILTROS DE EMPREENDIMENTO ===")
            print("(Filtros de preço e metragem estão em Unidades)")
            cidade   = input("Cidade (ENTER para ignorar): ").strip()
            regiao   = input("Região (ENTER para ignorar): ").strip()
            status   = input("Status (em obras/pronto/entregue): ").strip()
            lancamento = input("Período de lançamento (ENTER para ignorar): ").strip()
            ordenar  = input("Ordenar por (nome/cidade/regiao/entrega): ").strip()
            ordem    = input("Ordem (asc/desc) [asc]: ").strip() or "asc"

            args = ["consultar"]
            if cidade:     args += ["--cidade", cidade]
            if regiao:     args += ["--regiao", regiao]
            if status:     args += ["--status", status]
            if lancamento: args += ["--lancamento", lancamento]
            if ordenar:    args += ["--ordenar-por", ordenar]
            args += ["--ordem", ordem]

            _cli_empreendimento(args)
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            emp_id = input("\nID do empreendimento: ").strip()
            if emp_id.isdigit():
                _cli_empreendimento(["buscar", emp_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            _cli_empreendimento(["listar-disponiveis"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# UNIDADES (Sprint 10.5 — novo)
# ----------------------------------------------------------

def _cli_unidade(args: list):
    """Executa comando da CLI de unidades."""
    subprocess.run(["python", "-m", "src.interface.cli.unidade_cli"] + args)


def submenu_unidade():
    """Submenu de gerenciamento de unidades."""
    while True:
        cabecalho("UNIDADES")
        print("1 - Listar todas")
        print("2 - Buscar por ID")
        print("3 - Listar por empreendimento")
        print("4 - Marcar disponibilidade")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            _cli_unidade(["consultar"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            uni_id = input("\nID da unidade: ").strip()
            if uni_id.isdigit():
                _cli_unidade(["buscar", uni_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            emp_id = input("\nID do empreendimento: ").strip()
            if emp_id.isdigit():
                _cli_unidade(["listar-empreendimento", emp_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            uni_id = input("\nID da unidade: ").strip()
            print("Status: 1-disponível  2-vendido  3-reservado")
            status_op = input("Escolha: ").strip()
            status_map = {"1": "disponível", "2": "vendido", "3": "reservado"}
            status = status_map.get(status_op)
            if uni_id.isdigit() and status:
                _cli_unidade(["disponibilidade", uni_id, status])
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# MAILING
# ----------------------------------------------------------

def submenu_mailing():
    """Submenu de gerenciamento de mailing."""
    service = MailingService(MailingRepository(DB_PATH))

    while True:
        cabecalho("MAILING")
        print("1 - Consultar mailing")
        print("2 - Exportar mailing COMPLETO")
        print("3 - Exportar mailing RESUMIDO")
        print("4 - Rodar ingestão de mailing")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            registros = service.consultar()
            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for r in registros:
                    print(f"[{r.id}] {r.nome} — {r.email} — {r.telefone} "
                          f"— {r.origem} — score={r.score_mailing}")
                print(f"\nTotal: {len(registros)} registro(s).")
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            exporter = MailingExporterCompleto(service)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta = "data/exportacoes/mailing"
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, f"mailing_completo_{timestamp}.xlsx")
            exporter.exportar(caminho)
            print(f"\n✅ Exportado: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            exporter = MailingExporterResumido(service)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pasta = "data/exportacoes/mailing"
            os.makedirs(pasta, exist_ok=True)
            caminho = os.path.join(pasta, f"mailing_resumido_{timestamp}.xlsx")
            exporter.exportar(caminho)
            print(f"\n✅ Exportado: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            os.system("python -m src.infrastructure.ingestao.ingestao_mailing")
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# LEADS
# ----------------------------------------------------------

def submenu_lead():
    """Submenu de gerenciamento de leads."""
    from src.application.lead.services.lead_service import LeadService
    from src.infrastructure.lead.repositories.lead_repository import LeadRepository

    service = LeadService(LeadRepository(DB_PATH))

    while True:
        cabecalho("LEADS")
        print("1 - Consultar leads")
        print("2 - Rodar ingestão de leads")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            limpar_tela()
            registros = service.consultar()
            if not registros:
                print("Nenhum registro encontrado.")
            else:
                for r in registros:
                    print(f"[{r.id}] {r.nome} — {r.email} — {r.telefone} "
                          f"— {r.origem} — score={r.score_lead}")
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


# ----------------------------------------------------------
# MATCHING ENGINE
# ----------------------------------------------------------

def submenu_matching():
    """Submenu do Matching Engine (Sprint 9)."""
    while True:
        cabecalho("MATCHING ENGINE (Sprint 9)")
        print("1 - Matching para um lead")
        print("2 - Matching para todos os leads")
        print("3 - Listar matchings de um lead")
        print("4 - Melhores matchings de um lead")
        print("5 - Exportar matching de um lead (XLS)")
        print("6 - Exportar matching de TODOS os leads (XLS)")
        print("7 - Gerar mensagem para WhatsApp")
        print("0 - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        def _matching(args):
            subprocess.run(["python", "-m", "src.interface.cli.matching_cli"] + args)

        if opcao == "1":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                _matching(["run", "--lead-id", lead_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            _matching(["run-all"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                _matching(["list", "--lead-id", lead_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            lead_id = input("\nID do lead: ").strip()
            limit = input("Limite (padrão 5): ").strip() or "5"
            if lead_id.isdigit():
                _matching(["best", "--lead-id", lead_id, "--limit", limit])
            input("\nPressione ENTER para voltar...")

        elif opcao == "5":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                pasta = "data/exportacoes/matching"
                os.makedirs(pasta, exist_ok=True)
                caminho = f"{pasta}/lead_{lead_id}.xlsx"
                _matching(["export", "--lead-id", lead_id, "--out", caminho])
                print(f"\n✅ Exportado: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "6":
            pasta = "data/exportacoes/matching"
            os.makedirs(pasta, exist_ok=True)
            _matching(["export-all", "--out", pasta])
            print(f"\n✅ Exportados em: {pasta}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "7":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                _matching(["whatsapp", "--lead-id", lead_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# IA ENGINE
# ----------------------------------------------------------

def submenu_ia():
    """Submenu do IA Engine (Sprint 10)."""
    while True:
        cabecalho("IA ENGINE (Sprint 10)")
        print("1  - IA para um lead")
        print("2  - IA para todos os leads")
        print("3  - Listar IA de um lead")
        print("4  - Melhores IA de um lead")
        print("5  - Exportar IA de um lead (XLS)")
        print("6  - Exportar IA de TODOS os leads (XLS)")
        print("7  - Listar IA de TODOS os leads")
        print("8  - Dashboard IA (Painel Geral)")
        print("9  - Exportar Dashboard (XLS)")
        print("10 - Gerar mensagem para WhatsApp")
        print("0  - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        def _ia(args):
            subprocess.run(["python", "-m", "src.interface.cli.ia_cli"] + args)

        if opcao == "1":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                _ia(["run", "--lead-id", lead_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "2":
            _ia(["run-all"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "3":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                _ia(["list", "--lead-id", lead_id])
            input("\nPressione ENTER para voltar...")

        elif opcao == "4":
            lead_id = input("\nID do lead: ").strip()
            limit = input("Limite (padrão 5): ").strip() or "5"
            if lead_id.isdigit():
                _ia(["best", "--lead-id", lead_id, "--limit", limit])
            input("\nPressione ENTER para voltar...")

        elif opcao == "5":
            lead_id = input("\nID do lead: ").strip()
            if lead_id.isdigit():
                pasta = "data/exportacoes/ia"
                os.makedirs(pasta, exist_ok=True)
                caminho = f"{pasta}/lead_{lead_id}.xlsx"
                _ia(["export", "--lead-id", lead_id, "--out", caminho])
                print(f"\n✅ Exportado: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "6":
            pasta = "data/exportacoes/ia"
            os.makedirs(pasta, exist_ok=True)
            _ia(["export-all", "--out", pasta])
            print(f"\n✅ Exportados em: {pasta}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "7":
            _ia(["list-all"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "8":
            _ia(["dashboard"])
            input("\nPressione ENTER para voltar...")

        elif opcao == "9":
            pasta = "data/exportacoes/ia"
            os.makedirs(pasta, exist_ok=True)
            caminho = f"{pasta}/dashboard.xlsx"
            _ia(["export-dashboard", "--out", caminho])
            print(f"\n✅ Dashboard exportado: {caminho}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "10":
            lead_id = input("\nID do lead: ").strip()
            mode = input("Modo (curta/media/longa/premium) [premium]: ").strip() or "premium"
            if lead_id.isdigit():
                _ia(["whatsapp", "--lead-id", lead_id, "--mode", mode])
            input("\nPressione ENTER para voltar...")

        elif opcao == "0":
            return          # ← bug corrigido: estava faltando o return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# OFERTAS
# ----------------------------------------------------------

def submenu_offer():
    """Submenu do Offer Engine."""
    from src.interface.cli.offer_cli import OfferCLI
    from src.infrastructure.offer.exporters.offer_exporter_completo import OfferExporterCompleto

    cli = OfferCLI()
    exporter = OfferExporterCompleto(
        cli.service,
        cli.lead_repository,
        cli.empreendimento_repository
    )

    while True:
        cabecalho("OFERTAS")
        print("1  - Gerar ofertas para um lead")
        print("2  - Gerar ofertas para todos os leads")
        print("3  - Listar ofertas de um lead")
        print("4  - Relatório de ofertas para um lead")
        print("5  - Relatório de ofertas para todos os leads")
        print("6  - Exportar ofertas de um lead (XLS)")
        print("7  - Exportar ofertas de TODOS os leads (XLS)")
        print("8  - Gerar mensagem para WhatsApp")
        print("9  - Matching Engine")
        print("10 - IA Engine")
        print("0  - Voltar")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

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
            lead_id_str = input("\nID do lead: ").strip()
            if lead_id_str.isdigit():
                lead_id = int(lead_id_str)
                pasta = "data/exportacoes/ofertas"
                os.makedirs(pasta, exist_ok=True)
                caminho = os.path.join(pasta, f"lead_{lead_id}.xlsx")
                try:
                    exporter.exportar_por_lead(lead_id, caminho)
                    print(f"\n✅ Exportado: {caminho}")
                except Exception as e:
                    print(f"\n❌ Erro ao exportar: {e}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "7":
            pasta = "data/exportacoes/ofertas"
            os.makedirs(pasta, exist_ok=True)
            try:
                arquivos = exporter.exportar_todos(pasta)
                print(f"\n✅ {len(arquivos)} arquivo(s) gerado(s) em: {pasta}")
            except Exception as e:
                print(f"\n❌ Erro ao exportar: {e}")
            input("\nPressione ENTER para voltar...")

        elif opcao == "8":
            lead_id_str = input("\nID do lead: ").strip()
            if lead_id_str.isdigit():
                lead_id = int(lead_id_str)
                msg = cli.whatsapp_formatter.gerar_mensagem(lead_id)
                print("\n=== MENSAGEM PARA WHATSAPP ===\n")
                print(msg)
                print("\n(Copie e cole no WhatsApp)")
            input("\nPressione ENTER para voltar...")

        elif opcao == "9":
            submenu_matching()

        elif opcao == "10":
            submenu_ia()

        elif opcao == "0":
            return

        else:
            print("Opção inválida.")
            input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------
# MENU PRINCIPAL
# ----------------------------------------------------------

def main():
    while True:
        cabecalho("CORRETOR PLATFORM")
        print("1 - Ingestão de dados")
        print("2 - Empreendimentos")
        print("3 - Unidades")          # Sprint 10.5
        print("4 - Mailing")
        print("5 - Leads")
        print("6 - Ofertas / Engines")
        print("0 - Sair")
        print("=" * 45)

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            submenu_ingestao()
        elif opcao == "2":
            submenu_empreendimento()
        elif opcao == "3":
            submenu_unidade()
        elif opcao == "4":
            submenu_mailing()
        elif opcao == "5":
            submenu_lead()
        elif opcao == "6":
            submenu_offer()
        elif opcao == "0":
            print("\nSaindo...")
            sys.exit(0)
        else:
            print("\nOpção inválida.")
            input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()