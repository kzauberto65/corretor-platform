from difflib import SequenceMatcher

class MatchingEngine:

    def __init__(self):
        self.pesos = {
            "cidade": 0.25,
            "regiao": 0.20,
            "bairro": 0.15,
            "tipo": 0.15,
            "tipologia": 0.10,
            "quartos": 0.10,
            "metragem": 0.10,
            "preco": 0.20,
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
    # Matching principal
    # ---------------------------------------------------------
    def calculate_score_and_rationale(self, lead, emp):

        score = 0
        rationale = []

        # =====================================================
        # 1) CIDADE — obrigatório (comparação direta)
        # =====================================================
        cidade_emp = self._safe_str(self._get(emp, "cidade"))
        cidade_lead = self._safe_str(lead.get("cidade_interesse"))

#        print("\n===== DEBUG CIDADE =====")
#        print("EMP ID:", getattr(emp, "id", None))
#        print("cidade_emp (raw):", repr(self._get(emp, "cidade")))
#        print("cidade_emp (safe):", repr(self._safe_str(self._get(emp, "cidade"))))

#        print("lead:", lead)
#        print("cidade_lead (raw):", repr(lead.get("cidade_interesse")))
#        print("cidade_lead (safe):", repr(self._safe_str(lead.get("cidade_interesse"))))
#        print("========================\n")


        if cidade_emp != cidade_lead:
            return 0, "Cidade diferente — não ofertar"

        score += self.pesos["cidade"]
        rationale.append("Cidade compatível")

        # =====================================================
        # 2) REGIÃO — fuzzy
        # =====================================================
        regiao_emp = self._safe_str(self._get(emp, "regiao"))
        regiao_lead = self._safe_str(lead.get("regiao_interesse"))

        if self._similar(regiao_emp, regiao_lead) >= 0.6:
            score += self.pesos["regiao"]
            rationale.append("Região compatível")

        # =====================================================
        # 3) BAIRRO — fuzzy
        # =====================================================
        bairro_emp = self._safe_str(self._get(emp, "bairro"))
        bairro_lead = self._safe_str(lead.get("bairro_interesse"))

        if self._similar(bairro_emp, bairro_lead) >= 0.7:
            score += self.pesos["bairro"]
            rationale.append("Bairro compatível")

        # =====================================================
        # 4) TIPO DE IMÓVEL
        # =====================================================
        tipo_emp = self._safe_str(self._get(emp, "tipo"))
        tipo_lead = self._safe_str(lead.get("tipo_imovel"))

        if tipo_lead in tipo_emp or tipo_emp in tipo_lead:
            score += self.pesos["tipo"]
            rationale.append("Tipo compatível")

        # =====================================================
        # 5) TIPOLOGIA
        # =====================================================
        tip_emp = self._safe_str(self._get(emp, "tipologia"))

        if self._similar(tip_emp, tipo_lead) >= 0.5:
            score += self.pesos["tipologia"]
            rationale.append("Tipologia compatível")

        # =====================================================
        # 6) QUARTOS
        # =====================================================
        q_emp = self._safe_float(self._get(emp, "quartos"))
        q_lead = self._safe_float(lead.get("quartos"))

        if q_emp and q_lead and abs(q_emp - q_lead) <= 1:
            score += self.pesos["quartos"]
            rationale.append("Quartos próximos")

        # =====================================================
        # 7) METRAGEM
        # =====================================================
        mmin = self._safe_float(self._get(emp, "metragem_min"))
        mmax = self._safe_float(self._get(emp, "metragem_max"))
        lmin = self._safe_float(lead.get("metragem_min"))
        lmax = self._safe_float(lead.get("metragem_max"))

        if mmin and mmax and lmin and lmax:
            if mmax >= lmin * 0.7 and mmin <= lmax * 1.3:
                score += self.pesos["metragem"]
                rationale.append("Metragem compatível")

        # =====================================================
        # 8) PREÇO
        # =====================================================
        preco = self._safe_float(self._get(emp, "preco"))
        pmin = self._safe_float(lead.get("preco_min"), 0)
        pmax = self._safe_float(lead.get("preco_max"), 999999999)

        if pmin <= preco <= pmax:
            score += self.pesos["preco"]
            rationale.append("Preço dentro da faixa")

        return round(score, 3), "; ".join(rationale)
