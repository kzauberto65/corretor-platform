# src/interface/cli/ia_cli.py

import argparse

# ENGINE + SERVICE
from src.application.ia.engine.ia_engine import IAEngine
from src.application.ia.services.ia_service import IAService

# REPOSITORIES
from src.infrastructure.ia.repositories.ia_repository import IARepository
from src.infrastructure.lead.repositories.lead_repository import LeadRepository
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository

# EXPORTADORES
from src.infrastructure.ia.exporters.ia_exporter import IAExporter
from src.infrastructure.ia.exporters.ia_exporter_completo import IAExporterCompleto


def build_service():
    ia_repo = IARepository()
    lead_repo = LeadRepository()
    prop_repo = EmpreendimentoRepository()
    engine = IAEngine()

    return IAService(
        ia_repo=ia_repo,
        ia_engine=engine,
        lead_repo=lead_repo,
        property_repo=prop_repo
    )


def main():
    parser = argparse.ArgumentParser(prog="ia")
    sub = parser.add_subparsers(dest="command")

    # -------------------------
    # IA
    # -------------------------
    run = sub.add_parser("run")
    run.add_argument("--lead-id", type=int, required=True)

    sub.add_parser("run-all")

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--lead-id", type=int, required=True)

    best_cmd = sub.add_parser("best")
    best_cmd.add_argument("--lead-id", type=int, required=True)
    best_cmd.add_argument("--limit", type=int, default=5)

    # NOVO: LISTAR TODOS OS LEADS
    sub.add_parser("list-all")

    # NOVO: DASHBOARD
    sub.add_parser("dashboard")

    # PARA WHATSAPP
    whats = sub.add_parser("whatsapp")
    whats.add_argument("--lead-id", type=int, required=True)
    whats.add_argument("--mode", type=str, default="premium", choices=["curta", "media", "longa", "premium"])


    # -------------------------
    # EXPORTAÇÃO
    # -------------------------
    export_cmd = sub.add_parser("export")
    export_cmd.add_argument("--lead-id", type=int, required=True)
    export_cmd.add_argument("--out", type=str, required=True)

    export_all_cmd = sub.add_parser("export-all")
    export_all_cmd.add_argument("--out", type=str, required=True)

    export_dash = sub.add_parser("export-dashboard")
    export_dash.add_argument("--out", type=str, required=True)

    args = parser.parse_args()
    service = build_service()

    # Exportadores
    exporter = IAExporter(service, service.lead_repo, service.property_repo)
    exporter_completo = IAExporterCompleto(service, service.lead_repo, service.property_repo)

    # -------------------------
    # COMANDOS
    # -------------------------
    if args.command == "run":
        result = service.run_for_lead(args.lead_id)
        print(f"\nIA executada para o lead {result['lead_id']}")
        print(f"Total de resultados salvos: {result['total']}")
        print(f"Conversão média: {result['average_conversion']}\n")

    elif args.command == "run-all":
        service.run_all()
        print("\nIA executada para todos os leads.\n")

    elif args.command == "list":
        results = service.ia_repo.list_by_lead(args.lead_id)

        print(f"\nResultados de IA do lead {args.lead_id}:")
        if not results:
            print("Nenhum resultado encontrado.\n")
            return

        for r in results:
            print(f"- Property {r.property_id} | Similarity={r.similarity:.3f} | Conv={r.conversion_score:.2f}% | {r.created_at}")
        print()

    elif args.command == "best":
        results = service.ia_repo.list_best(args.lead_id, args.limit)

        print(f"\nTop {args.limit} resultados de IA do lead {args.lead_id}:")
        if not results:
            print("Nenhum resultado encontrado.\n")
            return

        for r in results:
            print(f"- Property {r.property_id} | Similarity={r.similarity:.3f} | Conv={r.conversion_score:.2f}% | {r.created_at}")
        print()

    # -------------------------
    # NOVO: LISTAR TODOS OS LEADS
    # -------------------------
    elif args.command == "list-all":
        leads = service.lead_repo.consultar()

        print("\n📌 IA — Lista completa por lead\n")

        for lead in leads:
            results = service.ia_repo.list_by_lead(lead.id)

            print(f"Lead {lead.id} — {len(results)} imóveis avaliados")

            if not results:
                print("  (nenhum resultado)\n")
                continue

            for r in results[:5]:  # mostra só os 5 primeiros
                print(f"  - Property {r.property_id} | Sim={r.similarity:.3f} | Conv={r.conversion_score:.2f}%")

            print()

    # -------------------------
    # NOVO: DASHBOARD
    # -------------------------
    elif args.command == "dashboard":
        leads = service.lead_repo.consultar()

        print("\n📊 DASHBOARD IA — Visão Geral\n")
        print("LEAD                  | MELHOR IMÓVEL                 | SCORE  | STATUS        | IMÓVEIS AVALIADOS | SCORE MÉDIO")
        print("---------------------------------------------------------------------------------------------------------------")

        for lead in leads:
            lead_nome = lead.nome if hasattr(lead, "nome") else f"Lead {lead.id}"

            best = service.ia_repo.list_best(lead.id, 1)
            all_scores = service.ia_repo.list_by_lead(lead.id)

            if not all_scores:
                print(f"{lead_nome:<22} | ---                          | ---    | SEM DADOS     | 0                  | 0")
                continue

            best_score = best[0].conversion_score if best else 0
            best_prop_id = best[0].property_id if best else None

            # Buscar nome do empreendimento
            prop = service.property_repo.find_by_id(best_prop_id)
            prop_nome = prop.nome if prop else f"Imóvel {best_prop_id}"

            avg = sum(r.conversion_score for r in all_scores) / len(all_scores)

            # STATUS
            if best_score >= 40:
                status = "🔥 ALTA"
            elif best_score >= 20:
                status = "⭐ MÉDIA"
            else:
                status = "❄️ BAIXA"

            print(f"{lead_nome:<22} | {prop_nome:<30} | {best_score:>5.1f}% | {status:<12} | {len(all_scores):<18} | {avg:>10.1f}%")

        print()


    # -------------------------
    # EXPORTAÇÃO
    # -------------------------
    elif args.command == "export":
        caminho = exporter.exportar(args.lead_id, args.out)
        print(f"\nArquivo exportado: {caminho}\n")

    elif args.command == "export-all":
        arquivos = exporter_completo.exportar_todos(args.out)
        print(f"\n{len(arquivos)} arquivos gerados em: {args.out}\n")
    
    elif args.command == "export-dashboard":
        from src.infrastructure.ia.exporters.ia_dashboard_exporter import IADashboardExporter
        exporter = IADashboardExporter(service)
        caminho = exporter.exportar(args.out)
        print(f"\nDashboard exportado: {caminho}\n")


    # WAHTSAPP
    elif args.command == "whatsapp":
        from src.infrastructure.ia.exporters.ia_whatsapp import IAWhatsAppExporter
        exporter = IAWhatsAppExporter(service)
        texto = exporter.gerar(args.lead_id, args.mode)
        print("\n=== MENSAGEM WHATSAPP ===\n")
        print(texto)
        print("\n==========================\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
