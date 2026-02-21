from typing import Any, Dict

class MatchingEngine:
    def match(self, lead, prop) -> tuple[float, Dict[str, Any]]:
        reasons: Dict[str, str] = {}

        # --- CIDADE (regra absoluta) ---
        if not lead.cidade_interesse or not prop.cidade:
            return 0.0, {"cidade": "Cidade não informada no lead ou no imóvel"}

        if lead.cidade_interesse != prop.cidade:
            return 0.0, {"cidade": "Cidade diferente"}

        reasons["cidade"] = "Mesma cidade"
        match_cidade = 1.0

        # --- BAIRRO OU REGIÃO (regra de prioridade) ---
        match_bairro = 0.0
        match_regiao = 0.0

        if lead.bairro_interesse:
            # BAIRRO É A REFERÊNCIA PRINCIPAL
            if prop.bairro == lead.bairro_interesse:
                match_bairro = 1.0
                reasons["bairro"] = "Mesmo bairro"
            else:
                reasons["bairro"] = "Bairro diferente"

            # região vira secundária
            if lead.regiao_interesse and prop.regiao:
                if lead.regiao_interesse == prop.regiao:
                    match_regiao = 0.5
                    reasons["regiao"] = "Região compatível (fallback)"
                else:
                    reasons["regiao"] = "Região diferente"

        else:
            # SE NÃO INFORMOU BAIRRO → REGIÃO É A REFERÊNCIA PRINCIPAL
            if lead.regiao_interesse and prop.regiao:
                if lead.regiao_interesse == prop.regiao:
                    match_regiao = 1.0
                    reasons["regiao"] = "Mesma região"
                else:
                    reasons["regiao"] = "Região diferente"
            else:
                reasons["regiao"] = "Região não informada"

        # --- PREÇO ---
        match_preco = 0.0
        if lead.preco_min is not None and lead.preco_max is not None:
            if lead.preco_min <= prop.preco <= lead.preco_max:
                match_preco = 1.0
                reasons["preco"] = "Dentro da faixa"
            else:
                reasons["preco"] = "Fora da faixa"
        else:
            reasons["preco"] = "Faixa não informada"

        # --- TIPOLOGIA ---
        match_tipo = 1.0 if (
            lead.tipo_imovel and prop.tipo and lead.tipo_imovel.lower() == prop.tipo.lower()
        ) else 0.0
        reasons["tipo"] = "Tipo compatível" if match_tipo else "Tipo diferente"

        # --- METRAGEM ---
        match_metragem = 0.0
        if lead.metragem_min is not None and lead.metragem_max is not None:
            if lead.metragem_min <= prop.metragem_min <= lead.metragem_max:
                match_metragem = 1.0
                reasons["metragem"] = "Metragem compatível"
            else:
                reasons["metragem"] = "Metragem fora da faixa"
        else:
            reasons["metragem"] = "Metragem não informada"

        # --- SCORE FINAL ---
        score_0_1 = (
            0.30 * match_preco +
            0.20 * match_cidade +
            0.25 * match_bairro +   # BAIRRO MAIS FORTE
            0.15 * match_regiao +   # REGIÃO FALLBACK
            0.10 * match_tipo +
            0.05 * match_metragem
        )

        score_0_100 = round(score_0_1 * 100, 2)
        return score_0_100, reasons
