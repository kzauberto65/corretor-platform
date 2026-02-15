from difflib import SequenceMatcher

class MatchingEngine:

    def __init__(self):
        # Pesos base (somam 1.0)
        self.pesos = {
            "cidade": 0.25,
            "regiao": 0.15,
            "bairro": 0.10,
            "tipo": 0.15,
            "tipologia": 0.10,
            "quartos": 0.10,
            "metragem": 0.10,
            "preco": 0.15,
        }

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _similar(self, a, b):
        if not a or not b:
            return 0
        return SequenceMatcher(None, a, b).ratio()

    def _safe_str(self, v):
        return str(v).strip().lower() if v else ""

    def _safe_float(self, v, default=None):
        try:
            return float(v)
        except:
            return default

    def _get(self, obj, field, default=None):
        return getattr(obj, field, default)

    # ---------------------------------------------------------
    # Matching principal — Sprint 9 GOLD
    # ---------------------------------------------------------
    def calculate_score_and_rationale(self, lead, emp):

        score = 0
        rationale = []
        penalties = 0
        boosts = 0

        # =====================================================
        # 1) CIDADE — obrigatório
        # =====================================================
        cidade_emp = self._safe_str(self._get(emp, "cidade"))
        cidade_lead = self._safe_str(lead.get("cidade_interesse"))

        if cidade_lead and cidade_emp != cidade_lead:
            return 0, "Cidade diferente — não ofertar"

        score += self.pesos["cidade"]
        rationale.append("Cidade compatível")

        # =====================================================
        # 2) REGIÃO — fuzzy
        # =====================================================
        regiao_emp = self._safe_str(self._get(emp, "regiao"))
        regiao_lead = self._safe_str(lead.get("regiao_interesse"))

        sim_regiao = self._similar(regiao_emp, regiao_lead)

        if regiao_lead:
            if sim_regiao >= 0.6:
                score += self.pesos["regiao"]
                rationale.append("Região compatível")
            else:
                penalties += 0.05
                rationale.append("Região distante")

        # =====================================================
        # 3) BAIRRO — fuzzy
        # =====================================================
        bairro_emp = self._safe_str(self._get(emp, "bairro"))
        bairro_lead = self._safe_str(lead.get("bairro_interesse"))

        sim_bairro = self._similar(bairro_emp, bairro_lead)

        if bairro_lead:
            if sim_bairro >= 0.7:
                score += self.pesos["bairro"]
                rationale.append("Bairro compatível")
            else:
                penalties += 0.05
                rationale.append("Bairro diferente")

        # =====================================================
        # 4) TIPO DE IMÓVEL
        # =====================================================
        tipo_emp = self._safe_str(self._get(emp, "tipo"))
        tipo_lead = self._safe_str(lead.get("tipo_imovel"))

        if tipo_lead and (tipo_lead in tipo_emp or tipo_emp in tipo_lead):
            score += self.pesos["tipo"]
            rationale.append("Tipo compatível")
        else:
            penalties += 0.05

        # =====================================================
        # 5) TIPOLOGIA
        # =====================================================
        tip_emp = self._safe_str(self._get(emp, "tipologia"))

        if tipo_lead and self._similar(tip_emp, tipo_lead) >= 0.5:
            score += self.pesos["tipologia"]
            rationale.append("Tipologia compatível")

        # =====================================================
        # 6) QUARTOS
        # =====================================================
        q_emp = self._safe_float(self._get(emp, "quartos"))
        q_lead = self._safe_float(lead.get("quartos"))

        if q_emp and q_lead:
            if abs(q_emp - q_lead) <= 1:
                score += self.pesos["quartos"]
                rationale.append("Quartos próximos")
            else:
                penalties += 0.10
                rationale.append("Número de quartos distante")

        # =====================================================
        # 7) METRAGEM — faixa do empreendimento deve caber na faixa do lead
        # =====================================================
        mmin = self._safe_float(self._get(emp, "metragem_min"))
        mmax = self._safe_float(self._get(emp, "metragem_max"))
        lmin = self._safe_float(lead.get("metragem_min"))
        lmax = self._safe_float(lead.get("metragem_max"))

        if mmin and mmax and lmin and lmax:
            if mmin >= lmin and mmax <= lmax:
                score += self.pesos["metragem"]
                rationale.append("Metragem compatível")

                # Boost leve (Sprint 9)
                if abs(mmin - lmin) <= 5 or abs(mmax - lmax) <= 5:
                    boosts += 0.05
                    rationale.append("Metragem muito próxima do ideal")
            else:
                penalties += 0.10
                rationale.append("Metragem fora da faixa")

        # =====================================================
        # 8) PREÇO — dentro da faixa do lead
        # =====================================================
        preco = self._safe_float(self._get(emp, "preco"))
        pmin = self._safe_float(lead.get("preco_min"), 0)
        pmax = self._safe_float(lead.get("preco_max"), 999999999)

        if preco:
            if pmin <= preco <= pmax:
                score += self.pesos["preco"]
                rationale.append("Preço dentro da faixa")

                # Boost leve (Sprint 9)
                if abs(preco - pmax) <= 50000:
                    boosts += 0.05
                    rationale.append("Preço muito próximo do ideal")
            else:
                penalties += 0.15
                rationale.append("Preço fora da faixa")

        # =====================================================
        # 9) URGÊNCIA — ajuste leve
        # =====================================================
        urgencia = self._safe_str(lead.get("urgencia"))

        multiplicador = {
            "alta": 1.1,
            "media": 1.0,
            "baixa": 0.9
        }.get(urgencia, 1.0)

        # =====================================================
        # SCORE FINAL
        # =====================================================
        final = score + boosts - penalties
        final *= multiplicador

        # Normalização
        final = max(0, min(1, final))

        return round(final, 3), "; ".join(rationale)
