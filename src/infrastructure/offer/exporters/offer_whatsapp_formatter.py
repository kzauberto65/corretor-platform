class OfferWhatsAppFormatter:

    def __init__(self, lead_repository, offer_repository, empreendimento_repository):
        self.lead_repository = lead_repository
        self.offer_repository = offer_repository
        self.empreendimento_repository = empreendimento_repository

    def gerar_mensagem(self, lead_id: int):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            return f"Lead {lead_id} não encontrado."

        ofertas = self.offer_repository.find_by_lead(lead_id)
        if not ofertas:
            return f"Não encontrei ofertas para o lead {lead_id}."

        ofertas = sorted(ofertas, key=lambda o: o.score, reverse=True)
        top = ofertas[:5]

        msg = []
        msg.append(f"*Ofertas para {lead.nome}*")
        msg.append(f"Faixa: R$ {lead.preco_min} a R$ {lead.preco_max}")
        msg.append(f"Cidade de interesse: {lead.cidade_interesse}")
        msg.append("")

        for o in top:
            emp = self.empreendimento_repository.find_by_id(o.empreendimento_id)

            msg.append(f"🏢 *{emp.nome}*")
            msg.append(f"📍 Endereço: {emp.endereco}")
            msg.append(f"📌 Bairro: {emp.bairro}")
            msg.append(f"📍 Região: {emp.regiao}")
            msg.append(f"🌆 Cidade: {emp.cidade}")
            msg.append(f"💰 Preço: R$ {emp.preco}")
            msg.append(f"📅 Entrega: {emp.data_entrega}")
            msg.append(f"📝 Descrição: {emp.descricao}")
#            msg.append(f"⭐ Score: {o.score:.2f}")
#            msg.append(f"🔎 Critérios: {o.rationale}")
            msg.append("")

        return "\n".join(msg)
