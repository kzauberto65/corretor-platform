import json
from pathlib import Path
from src.application.offer.matching.matching_engine import MatchingEngine

# Dummy class para simular um empreendimento
class DummyEmp:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_batch_test():
    print("\n=== TESTE EM LOTE DO MATCHING ENGINE (SPRINT 9) ===\n")

    base = Path("tests/data")
    leads = load_json(base / "leads.json")
    empreendimentos = load_json(base / "empreendimentos.json")

    engine = MatchingEngine()

    for lead in leads:
        print(f"\n---------------------------------------------")
        print(f"LEAD {lead['id']} — {lead['nome']}")
        print(f"Interesse: {lead['bairro_interesse']} / {lead['regiao_interesse']} / {lead['cidade_interesse']}")
        print("---------------------------------------------\n")

        resultados = []

        for emp_data in empreendimentos:
            emp = DummyEmp(**emp_data)
            score, rationale = engine.calculate_score_and_rationale(lead, emp)
            resultados.append((emp.id, score, rationale, emp))

        # Ordenar por score
        resultados.sort(key=lambda x: x[1], reverse=True)

        # Mostrar top 5
        print("TOP MATCHES:")
        for emp_id, score, rationale, emp in resultados[:5]:
            print(f"  Emp {emp_id} | Score={score} | {emp.bairro}, {emp.regiao} | {rationale}")

        print("\nTodos os resultados:")
        for emp_id, score, rationale, emp in resultados:
            print(f"  Emp {emp_id} | Score={score} | {rationale}")

    print("\n=== FIM DO TESTE EM LOTE ===\n")


if __name__ == "__main__":
    run_batch_test()
