class MatchingWhatsAppFormatter:

    def __init__(self, lead_repository, matching_repository, empreendimento_repository):
        self.lead_repository = lead_repository
        self.matching_repository = matching_repository
        self.empreendimento_repository = empreendimento_repository

    def gerar_mensagem(self, lead_id: int):
        lead = self.lead_repository.buscar_por_id(lead_id)
        if not lead:
            return f"Lead {lead_id} não encontrado."

        matchings = self.matching_repository.list_by_lead(lead_id)
        if not matchings:
            return f"Não encontrei matchings para o lead {lead_id}."

        matchings = sorted(matchings, key=lambda m: m.score, reverse=True)
        top = matchings[:5]

        msg = []
        msg.append(f"*Matchings para {lead.nome}*")
        msg.append(f"Faixa: R$ {lead.preco_min} a R$ {lead.preco_max}")
        msg.append(f"Cidade de interesse: {lead.cidade_interesse}")
        msg.append("")

        for m in top:
            emp = self.empreendimento_repository.find_by_id(m.property_id)

            msg.append(f"🏢 *{emp.nome}*")
            msg.append(f"📍 Endereço: {emp.endereco}")
            msg.append(f"📌 Bairro: {emp.bairro}")
            msg.append(f"📍 Região: {emp.regiao}")
            msg.append(f"🌆 Cidade: {emp.cidade}")
            msg.append(f"💰 Preço: R$ {emp.preco}")
            msg.append(f"📅 Entrega: {emp.data_entrega}")
            msg.append(f"📝 Descrição: {emp.descricao}")
            msg.append(f"⭐ Score: {m.score:.2f}")

            # RATIONALE FORMATADO
            if m.reasons_json:
                msg.append("🔎 *Por que recomendamos:*")
                for motivo in m.reasons_json:
                    msg.append(f"   • {motivo}")

            msg.append("")

        return "\n".join(msg)
