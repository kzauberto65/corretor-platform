class IAWhatsAppExporter:

    def __init__(self, service):
        self.service = service

    def gerar(self, lead_id: int, mode: str = "premium") -> str:
        lead = self.service.lead_repo.buscar_por_id(lead_id)
        lead_nome = getattr(lead, "nome", f"Lead {lead_id}")

        best = self.service.ia_repo.list_best(lead_id, 1)
        if not best:
            return f"Olá {lead_nome}, tudo bem? Ainda estou separando as melhores opções para você. Já te aviso!"

        item = best[0]

        # Buscar nome do empreendimento
        prop = self.service.property_repo.find_by_id(item.property_id)
        prop_nome = getattr(prop, "nome", f"Imóvel {item.property_id}")

        reasons = item.reasons_json

        # Dados formatados
        localizacao = reasons.get("localizacao", "informação não disponível")
        preco = reasons.get("preco", "informação não disponível")
        metragem = reasons.get("metragem", "informação não disponível")
        entrega = reasons.get("entrega", "informação não disponível")
        urgencia = reasons.get("urgencia", "informação não disponível")

        # -------------------------
        # MENSAGENS POR MODO
        # -------------------------

        if mode == "curta":
            return (
                f"Olá {lead_nome}! Separei um imóvel que combina muito com o que você está buscando.\n\n"
                f"🏡 *{prop_nome}*\n\n"
                f"Destaques:\n"
                f"• Localização: {localizacao}\n"
                f"• Preço: {preco}\n"
                f"• Metragem: {metragem}\n"
                f"• Entrega: {entrega}\n\n"
                f"Quer que eu te envie fotos, vídeo ou mais detalhes?"
            )

        if mode == "media":
            return (
                f"Olá {lead_nome}! Analisei seu perfil e encontrei um imóvel que se encaixa muito bem no que você procura.\n\n"
                f"🏡 *{prop_nome}*\n\n"
                f"Motivos da recomendação:\n"
                f"• Localização: {localizacao}\n"
                f"• Preço: {preco}\n"
                f"• Metragem: {metragem}\n"
                f"• Entrega: {entrega}\n"
#                f"• Urgência: {urgencia}\n\n"
                f"Posso te enviar fotos, vídeo, planta ou agendar uma visita."
            )

        if mode == "longa":
            return (
                f"Olá {lead_nome}! Fiz uma análise completa do que você está buscando e encontrei um imóvel que realmente se destaca.\n\n"
                f"🏡 *Imóvel recomendado*: {prop_nome}\n\n"
                f"Por que ele combina com você:\n"
                f"• Localização: {localizacao}\n"
                f"• Preço: {preco}\n"
                f"• Metragem: {metragem}\n"
                f"• Entrega: {entrega}\n"
#                f"• Urgência: {urgencia}\n\n"
                f"Esse imóvel se destacou entre várias opções que avaliei.\n"
                f"Se quiser, posso te enviar fotos, vídeo, planta, condições especiais ou agendar uma visita."
            )

        # -------------------------
        # PREMIUM (versão escolhida)
        # -------------------------
        return (
            f"Olá {lead_nome}! Analisei cuidadosamente o que você está buscando e encontrei um imóvel que realmente se destaca como uma excelente opção para você.\n\n"
            f"🏡 *Imóvel recomendado*: {prop_nome}\n\n"
            f"Por que ele pode ser ideal para o seu perfil:\n"
            f"• 📍 Localização: {localizacao}\n"
            f"• 💰 Preço: {preco}\n"
            f"• 📐 Metragem: {metragem}\n"
            f"• 🏗️ Entrega: {entrega}\n"
#            f"• ⏱️ Urgência: {urgencia}\n\n"
            f"Esse imóvel se destacou entre várias opções que analisei e vale muito a pena conhecer.\n\n"
            f"Posso te enviar fotos, vídeo, planta, condições especiais ou agendar uma visita no melhor horário para você."
        )
