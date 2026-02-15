import argparse

from src.application.matching.engine.matching_engine import MatchingEngine
from src.application.matching.services.matching_service import MatchingService

from src.infrastructure.matching.repositories.matching_repository import MatchingRepository
from src.infrastructure.lead.repositories.lead_repository import LeadRepository
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository

# EXPORTADORES
from src.infrastructure.matching.exporters.matching_exporter import MatchingExporter
from src.infrastructure.matching.exporters.matching_exporter_completo import MatchingExporterCompleto

# WHATSAPP FORMATTER
from src.infrastructure.matching.exporters.matching_whatsapp_formatter import MatchingWhatsAppFormatter


def build_service():
    matching_repo = MatchingRepository()          # padrão igual Offer
    lead_repo = LeadRepository()
    prop_repo = EmpreendimentoRepository()
    engine = MatchingEngine()

    return MatchingService(
        matching_repo=matching_repo,
        matching_engine=engine,
        lead_repo=lead_repo,
        property_repo=prop_repo
    )


def main():
    parser = argparse.ArgumentParser(prog="matching")
    sub = parser.add_subparsers(dest="command")

    # -------------------------
    # MATCHING
    # -------------------------
    run = sub.add_parser("run")
    run.add_argument("--lead-id", type=int, required=True)

    sub.add_parser("run-all")

    list_cmd = sub.add_parser("list")
    list_cmd.add_argument("--lead-id", type=int, required=True)

    best_cmd = sub.add_parser("best")
    best_cmd.add_argument("--lead-id", type=int, required=True)
    best_cmd.add_argument("--limit", type=int, default=5)

    # -------------------------
    # EXPORTAÇÃO
    # -------------------------
    export_cmd = sub.add_parser("export")
    export_cmd.add_argument("--lead-id", type=int, required=True)
    export_cmd.add_argument("--out", type=str, required=True)

    export_all_cmd = sub.add_parser("export-all")
    export_all_cmd.add_argument("--out", type=str, required=True)

    # -------------------------
    # WHATSAPP
    # -------------------------
    whatsapp_cmd = sub.add_parser("whatsapp")
    whatsapp_cmd.add_argument("--lead-id", type=int, required=True)

    args = parser.parse_args()
    service = build_service()

    # Exportadores
    exporter = MatchingExporter(service, service.lead_repo, service.property_repo)
    exporter_completo = MatchingExporterCompleto(service, service.lead_repo, service.property_repo)

    # WhatsApp formatter
    formatter = MatchingWhatsAppFormatter(
        service.lead_repo,
        service.matching_repo,
        service.property_repo
    )

    # -------------------------
    # COMANDOS
    # -------------------------
    if args.command == "run":
        result = service.run_for_lead(args.lead_id)
        print(f"\nMatching executado para o lead {result.lead_id}")
        print(f"Total de matchings salvos: {result.total}")
        print(f"Score médio: {result.average_score}\n")

    elif args.command == "run-all":
        service.run_all()
        print("\nMatching executado para todos os leads.\n")

    elif args.command == "list":
        matchings = service.matching_repo.list_by_lead(args.lead_id)

        print(f"\nMatchings do lead {args.lead_id}:")
        if not matchings:
            print("Nenhum matching encontrado.\n")
            return

        for m in matchings:
            print(f"- Property {m.property_id} | Score={m.score} | {m.created_at}")
        print()

    elif args.command == "best":
        matchings = service.matching_repo.list_best_matches(args.lead_id, args.limit)

        print(f"\nTop {args.limit} matchings do lead {args.lead_id}:")
        if not matchings:
            print("Nenhum matching encontrado.\n")
            return

        for m in matchings:
            print(f"- Property {m.property_id} | Score={m.score} | {m.created_at}")
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

    # -------------------------
    # WHATSAPP
    # -------------------------
    elif args.command == "whatsapp":
        msg = formatter.gerar_mensagem(args.lead_id)
        print("\n=== MENSAGEM PARA WHATSAPP ===\n")
        print(msg)
        print("\n(Copie e cole no WhatsApp)\n")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
