from math import sqrt
from typing import Dict, Any
from datetime import datetime


class IAEngine:

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _safe_float(self, v, default=0.0) -> float:
        try:
            return float(v)
        except:
            return default

    def _safe_str(self, v) -> str:
        return str(v).strip().lower() if v else ""

    def _normalize_vector(self, vec: Dict[str, float]) -> Dict[str, float]:
        norm = sqrt(sum(v * v for v in vec.values())) or 1.0
        return {k: v / norm for k, v in vec.items()}

    def _cosine_similarity(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        dot = sum(v1.get(k, 0) * v2.get(k, 0) for k in v1.keys())
        return max(0.0, min(1.0, dot))

    # ---------------------------------------------------------
    # Data de entrega
    # ---------------------------------------------------------
    def _months_until(self, date_str) -> int:
        if not date_str:
            return 24
        try:
            dt = datetime.fromisoformat(str(date_str))
            now = datetime.now()
            diff = (dt.year - now.year) * 12 + (dt.month - now.month)
            return max(0, diff)
        except:
            return 24

    # ---------------------------------------------------------
    # Localização — regra mãe
    # ---------------------------------------------------------
    def _location_score(self, lead: Dict[str, Any], emp: Any) -> float:

        lead_cidade = self._safe_str(lead.get("cidade"))
        lead_regiao = self._safe_str(lead.get("regiao"))
        lead_bairro = self._safe_str(lead.get("bairro"))

        emp_cidade = self._safe_str(getattr(emp, "cidade", None))
        emp_regiao = self._safe_str(getattr(emp, "regiao", None))
        emp_bairro = self._safe_str(getattr(emp, "bairro", None))

        if lead_cidade and emp_cidade and lead_cidade != emp_cidade:
            return 0.0

        if lead_bairro and emp_bairro and lead_bairro == emp_bairro:
            return 1.0

        if lead_regiao and emp_regiao and lead_regiao == emp_regiao:
            return 0.7

        if lead_cidade and emp_cidade and lead_cidade == emp_cidade:
            return 0.4

        return 0.0

    # ---------------------------------------------------------
    # Normalização do lead (shim para campos *_interesse)
    # ---------------------------------------------------------
    def _normalize_lead_input(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        lead = dict(lead)  # cópia defensiva

        # mapeia campos de interesse para os usados na localização
        if not lead.get("cidade") and lead.get("cidade_interesse"):
            lead["cidade"] = lead.get("cidade_interesse")

        if not lead.get("bairro") and lead.get("bairro_interesse"):
            lead["bairro"] = lead.get("bairro_interesse")

        if not lead.get("regiao") and lead.get("regiao_interesse"):
            lead["regiao"] = lead.get("regiao_interesse")

        # garante que os campos numéricos existam (evita None)
        for k in ["preco_min", "preco_max", "metragem_min", "metragem_max"]:
            if lead.get(k) is None:
                lead[k] = 0

        return lead

    # ---------------------------------------------------------
    # Vetorização
    # ---------------------------------------------------------
    def _vectorize_lead(self, lead: Dict[str, Any]) -> Dict[str, float]:

        return {
            "preco_min": self._safe_float(lead.get("preco_min")) / 1_000_000,
            "preco_max": self._safe_float(lead.get("preco_max")) / 1_000_000,
            "metragem_min": self._safe_float(lead.get("metragem_min")) / 200,
            "metragem_max": self._safe_float(lead.get("metragem_max")) / 200,

            "urgencia": {
                "baixa": 0.2,
                "media": 0.5,
                "alta": 1.0
            }.get(self._safe_str(lead.get("urgencia")), 0.5),

            # preferência do lead: entrega imediata (placeholder)
            "preferencia_entrega": 0.0,
        }

    def _vectorize_property(self, emp: Any) -> Dict[str, float]:

        entrega_meses = self._months_until(getattr(emp, "data_entrega", None))

        return {
            "preco": self._safe_float(getattr(emp, "preco", 0)) / 1_000_000,
            "metragem_min": self._safe_float(getattr(emp, "metragem_min", 0)) / 200,
            "metragem_max": self._safe_float(getattr(emp, "metragem_max", 0)) / 200,

            # entrega normalizada
            "entrega": entrega_meses / 24,
        }

    # ---------------------------------------------------------
    # Conversão (similaridade + localização + urgência + entrega)
    # ---------------------------------------------------------
    def _predict_conversion(
        self,
        similarity: float,
        location_score: float,
        lead: Dict[str, Any],
        emp: Any
    ) -> float:

        urgencia = self._safe_str(lead.get("urgencia"))
        urg_factor = {
            "alta": 1.20,
            "media": 1.00,
            "baixa": 0.85
        }.get(urgencia, 1.00)

        entrega_meses = self._months_until(getattr(emp, "data_entrega", None))

        if urgencia == "alta":
            if entrega_meses == 0:
                entrega_factor = 1.25
            elif entrega_meses <= 6:
                entrega_factor = 1.05
            elif entrega_meses <= 12:
                entrega_factor = 0.85
            else:
                entrega_factor = 0.65
        else:
            if entrega_meses == 0:
                entrega_factor = 1.05
            elif entrega_meses <= 12:
                entrega_factor = 1.00
            else:
                entrega_factor = 0.90

        base = similarity * 0.5 + location_score * 0.4
        base = max(0.0, min(1.0, base))

        score = base * urg_factor * entrega_factor
        score = max(0.0, min(1.0, score))

        return round(score * 100, 2)

    # ---------------------------------------------------------
    # Rationale
    # ---------------------------------------------------------
    def _build_rationale(
        self,
        similarity,
        lead_vec,
        prop_vec,
        conversion_score,
        location_score,
        lead,
        emp
    ):

        if location_score >= 0.95:
            loc_txt = "Bairro exatamente como o desejado"
        elif location_score >= 0.65:
            loc_txt = "Região compatível com a desejada"
        elif location_score >= 0.35:
            loc_txt = "Cidade compatível, mas região/bairro diferentes"
        else:
            loc_txt = "Localização distante da preferência do lead"

        entrega_meses = self._months_until(getattr(emp, "data_entrega", None))

        if entrega_meses == 0:
            entrega_txt = "Imóvel pronto para morar"
        elif entrega_meses <= 6:
            entrega_txt = f"Entrega em aproximadamente {entrega_meses} meses"
        else:
            entrega_txt = f"Entrega mais longa (cerca de {entrega_meses} meses)"

        urgencia = self._safe_str(lead.get("urgencia"))

        if urgencia == "alta":
            urg_txt = f"Lead com alta urgência, entrega impactou fortemente o score final: {conversion_score:.2f}"
        else:
            urg_txt = f"Urgência considerada no score final: {conversion_score:.2f}"

        return {
            "similaridade": f"{similarity:.2f}",
            "localizacao": loc_txt,
            "preco": (
                "Faixa compatível"
                if lead_vec["preco_min"] <= prop_vec["preco"] <= lead_vec["preco_max"]
                else "Preço fora da faixa"
            ),
            "metragem": (
                "Dentro da faixa"
                if lead_vec["metragem_min"] <= prop_vec["metragem_min"] <= lead_vec["metragem_max"]
                else "Metragem distante"
            ),
            "entrega": entrega_txt,
            "urgencia": urg_txt,
        }

    # ---------------------------------------------------------
    # EXECUTAR
    # ---------------------------------------------------------
    def executar(self, lead: Dict[str, Any], emp: Any):

        # normaliza o lead (campos *_interesse → cidade/bairro/regiao)
        lead = self._normalize_lead_input(lead)

        print(
            "EMP DEBUG:",
            getattr(emp, "id", None),
            getattr(emp, "preco", None),
            getattr(emp, "metragem_min", None),
            getattr(emp, "metragem_max", None),
            getattr(emp, "data_entrega", None),
        )
        print(
            "LEAD DEBUG:",
            lead.get("preco_min"),
            lead.get("preco_max"),
            lead.get("metragem_min"),
            lead.get("metragem_max"),
            lead.get("cidade"),
            lead.get("bairro"),
            lead.get("regiao"),
            lead.get("urgencia"),
        )

        lead_vec_raw = self._vectorize_lead(lead)
        prop_vec_raw = self._vectorize_property(emp)

        lead_vec = self._normalize_vector(lead_vec_raw)
        prop_vec = self._normalize_vector(prop_vec_raw)

        similarity = self._cosine_similarity(lead_vec, prop_vec)
        location_score = self._location_score(lead, emp)

        conversion_score = self._predict_conversion(
            similarity=similarity,
            location_score=location_score,
            lead=lead,
            emp=emp
        )

        reasons = self._build_rationale(
            similarity=similarity,
            lead_vec=lead_vec_raw,
            prop_vec=prop_vec_raw,
            conversion_score=conversion_score,
            location_score=location_score,
            lead=lead,
            emp=emp
        )

        return similarity, conversion_score, lead_vec_raw, prop_vec_raw, reasons
