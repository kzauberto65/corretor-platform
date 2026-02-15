from typing import Any, Dict


class MatchingEngine:
    def match(self, lead, prop) -> tuple[float, Dict[str, Any]]:
        reasons: Dict[str, str] = {}

        # --- preço ---
        match_preco = 0.0
        if lead.preco_min is not None and lead.preco_max is not None:
            if lead.preco_min <= prop.preco <= lead.preco_max:
                match_preco = 1.0
                reasons["preco"] = "Dentro da faixa do lead"
            else:
                reasons["preco"] = "Fora da faixa do lead"
        else:
            reasons["preco"] = "Faixa de preço do lead não informada"

        # --- localização ---
        match_localizacao = 0.0
        if lead.cidade_interesse == prop.cidade:
            match_localizacao += 0.5
            reasons["localizacao"] = "Mesma cidade"
            if lead.regiao_interesse == prop.regiao:
                match_localizacao += 0.3
                reasons["localizacao"] = "Mesma cidade e região"
            if lead.bairro_interesse == prop.bairro:
                match_localizacao += 0.2
                reasons["localizacao"] = "Mesmo bairro de interesse"
        else:
            reasons["localizacao"] = "Cidade diferente"

        # --- tipologia / tipo ---
        match_tipologia = 0.0
        if lead.tipo_imovel and prop.tipo and lead.tipo_imovel.lower() == prop.tipo.lower():
            match_tipologia = 1.0
            reasons["tipologia"] = "Tipo compatível"
        else:
            reasons["tipologia"] = "Tipo diferente"

        # --- metragem ---
        match_metragem = 0.0
        if lead.metragem_min is not None and lead.metragem_max is not None:
            if lead.metragem_min <= prop.metragem_min <= lead.metragem_max:
                match_metragem = 1.0
                reasons["metragem"] = "Metragem compatível"
            else:
                reasons["metragem"] = "Metragem fora da faixa"
        else:
            reasons["metragem"] = "Metragem de interesse não informada"

        # --- renda / histórico (placeholder v1) ---
        match_renda = 0.0
        reasons["renda"] = "Heurística de renda ainda não implementada"

        match_historico = 0.0
        reasons["historico"] = "Histórico ainda não considerado"

        # fórmula v1 (0–1)
        score_0_1 = (
            0.35 * match_preco
            + 0.25 * match_localizacao
            + 0.15 * match_tipologia
            + 0.10 * match_metragem
            + 0.10 * match_renda
            + 0.05 * match_historico
        )

        score_0_100 = round(score_0_1 * 100, 2)
        return score_0_100, reasons
