class OfferReportService:
    def __init__(self, offer_repository, lead_repository, empreendimento_repository):
        self.offer_repository = offer_repository
        self.lead_repository = lead_repository
        self.empreendimento_repository = empreendimento_repository

    def generate_report_for_lead(self, lead_id: int):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            return f"Lead {lead_id} não encontrado."

        offers = self.offer_repository.find_by_lead(lead_id)
        if not offers:
            return f"Nenhuma oferta encontrada para o lead {lead_id}."

        # Ordena por score
        offers = sorted(offers, key=lambda o: o.score, reverse=True)

        # Cabeçalho
        report = []
        report.append("=" * 60)
        report.append(f"LEAD {lead.id} — {lead.nome}")
        report.append(f"Faixa de preço: {lead.preco_min} a {lead.preco_max}")
        report.append(f"Cidade: {lead.cidade_interesse}")
        report.append(f"Tipo de imóvel: {lead.tipo_imovel}")
        report.append(f"Urgência: {lead.urgencia}")
        report.append("-" * 60)
        report.append(f"Ofertas geradas: {len(offers)}\n")

        # Top 5
        report.append("TOP 5 OFERTAS")
        for o in offers[:5]:
            emp = self.empreendimento_repository.find_by_id(o.empreendimento_id)

            report.append(
                f"{o.empreendimento_id}) {emp.nome} — {emp.bairro}, {emp.cidade}\n"
                f"   Endereço: {emp.endereco}\n"
                f"   Score: {o.score:.3f}\n"
                f"   Rationale: {o.rationale}\n"
            )

        report.append("=" * 60)
        return "\n".join(report)

    def generate_report_for_all(self):
        leads = self.lead_repository.consultar()
        if not leads:
            return "Nenhum lead encontrado."

        full_report = []
        for lead in leads:
            full_report.append(self.generate_report_for_lead(lead.id))
            full_report.append("\n")

        return "\n".join(full_report)
