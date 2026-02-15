import pytest
from src.application.offer.matching.matching_engine import MatchingEngine

# Dummy class para simular um empreendimento
class DummyEmp:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

@pytest.fixture
def engine():
    return MatchingEngine()

@pytest.fixture
def lead():
    return {
        "cidade_interesse": "sao paulo",
        "regiao_interesse": "zona sul",
        "bairro_interesse": "moema",
        "tipo_imovel": "apartamento",
        "quartos": 2,
        "metragem_min": 40,
        "metragem_max": 60,
        "preco_min": 300000,
        "preco_max": 600000,
        "urgencia": "alta"
    }

def test_matching_score_alto(engine, lead):
    emp = DummyEmp(
        id=101,
        cidade="sao paulo",
        regiao="zona sul",
        bairro="moema",
        tipo="apartamento",
        tipologia="2 dorm",
        quartos=2,
        metragem_min=45,
        metragem_max=55,
        preco=550000
    )

    score, rationale = engine.calculate_score_and_rationale(lead, emp)

    print("\n[DEBUG] Score alto:", score, rationale)
    assert score > 0.7

def test_matching_score_medio(engine, lead):
    emp = DummyEmp(
        id=102,
        cidade="sao paulo",
        regiao="zona sul",
        bairro="vila mariana",
        tipo="apartamento",
        tipologia="2 dorm",
        quartos=3,
        metragem_min=70,
        metragem_max=90,
        preco=650000
    )

    score, rationale = engine.calculate_score_and_rationale(lead, emp)

    print("\n[DEBUG] Score médio:", score, rationale)
    assert 0 < score < 0.6

def test_matching_score_zero(engine, lead):
    emp = DummyEmp(
        id=103,
        cidade="campinas",
        regiao="centro",
        bairro="cambuí",
        tipo="apartamento",
        tipologia="2 dorm",
        quartos=2,
        metragem_min=50,
        metragem_max=60,
        preco=450000
    )

    score, rationale = engine.calculate_score_and_rationale(lead, emp)

    print("\n[DEBUG] Score zero:", score, rationale)
    assert score == 0
    assert "Cidade diferente" in rationale
