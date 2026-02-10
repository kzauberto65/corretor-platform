from src.application.offer.services.offer_service import OfferService
from src.application.offer.services.offer_report_service import OfferReportService
from src.infrastructure.offer.repositories.offer_repository import OfferRepository
from src.infrastructure.lead.repositories.lead_repository import LeadRepository
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.infrastructure.offer.exporters.offer_exporter import OfferExporter
from src.infrastructure.offer.exporters.offer_exporter_completo import OfferExporterCompleto
from src.infrastructure.offer.exporters.offer_whatsapp_formatter import OfferWhatsAppFormatter

class OfferCLI:
    def __init__(self):
        self.offer_repository = OfferRepository()
        self.lead_repository = LeadRepository()
        self.empreendimento_repository = EmpreendimentoRepository()

        self.service = OfferService(
            offer_repository=self.offer_repository,
            lead_repository=self.lead_repository,
            empreendimento_repository=self.empreendimento_repository
        )

        # Serviço de relatório integrado
        self.report_service = OfferReportService(
            self.offer_repository,
            self.lead_repository,
            self.empreendimento_repository
        )

        # Serviço de exportação integrado
        self.exporter = OfferExporter(
            self.service,
            self.lead_repository,
            self.empreendimento_repository
        )

        # Serviço de exportação completo integrado
        self.exporter = OfferExporterCompleto(
            self.service,
            self.lead_repository,
            self.empreendimento_repository
        )
        
        # Serviço de formatação para WhatsApp integrado
        self.whatsapp_formatter = OfferWhatsAppFormatter(
            self.lead_repository,
            self.offer_repository,
            self.empreendimento_repository
        )

    def generate_for_lead(self):
        lead_id_str = input("ID do lead: ").strip()

        if not lead_id_str.isdigit():
            print("ID inválido.")
            return

        lead_id = int(lead_id_str)
        count = self.service.generate_offers_for_lead(lead_id)

        print(f"{count} ofertas geradas para o lead {lead_id}.")

    def generate_for_all(self):
        count = self.service.generate_offers_for_all_leads()
        print(f"{count} ofertas geradas para todos os leads.")

    def list_by_lead(self):
        lead_id_str = input("ID do lead: ").strip()

        if not lead_id_str.isdigit():
            print("ID inválido.")
            return

        lead_id = int(lead_id_str)
        offers = self.offer_repository.find_by_lead(lead_id)

        if not offers:
            print("Nenhuma oferta encontrada para este lead.")
            return

        print(f"\nOfertas para o lead {lead_id}:\n")

        for offer in offers:
            emp = self.empreendimento_repository.find_by_id(offer.empreendimento_id)

            print(f"[{offer.id}] {emp.nome} — {emp.bairro}, {emp.cidade}")
            print(f"  Endereço: {emp.endereco}")
            print(f"  Score: {offer.score:.2f}")
            print(f"  Criado em: {offer.created_at}")
            print(f"  Rationale: {offer.rationale}")
            print("-" * 50)

    # Relatório para um lead
    def report_for_lead(self):
        lead_id_str = input("ID do lead: ").strip()

        if not lead_id_str.isdigit():
            print("ID inválido.")
            return

        lead_id = int(lead_id_str)
        report = self.report_service.generate_report_for_lead(lead_id)
        print("\n" + report + "\n")

    # Relatório para todos os leads
    def report_for_all(self):
        report = self.report_service.generate_report_for_all()
        print("\n" + report + "\n")

    # Exportar ofertas de um lead para Excel
    def export_xls(self):
        lead_id_str = input("ID do lead: ").strip()

        if not lead_id_str.isdigit():
            print("ID inválido.")
            return

        lead_id = int(lead_id_str)
        caminho = f"exports/ofertas_lead_{lead_id}.xlsx"

        try:
            arquivo = self.exporter.exportar(lead_id, caminho)
            print(f"Arquivo gerado: {arquivo}")
        except Exception as e:
            print(f"Erro ao exportar: {e}")
    
    # Exportar ofertas de todos os leads para Excel
    def export_all_xls(self):
        pasta = "exports/ofertas"
        try:
            arquivos = self.exporter.exportar_todos(pasta)
            print(f"{len(arquivos)} arquivos gerados em: {pasta}")
        except Exception as e:
            print(f"Erro ao exportar: {e}")

