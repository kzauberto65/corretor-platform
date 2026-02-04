import pytest
from src.application.unidade.services.unidade_service import UnidadeService
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository
from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO

@pytest.fixture
def service():
    repo = UnidadeRepository()
    return UnidadeService(repo)

def test_cadastrar(service):
    dto = UnidadeInputDTO(
        empreendimento_id=1,
        construtora_id=1,
        codigo_unidade="A101",
        metragem=75.5,
        valor=350000.00,
        observacoes="Unidade teste",
        tipo_unidade_id=1   # <-- agora carrega 'Apto'
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.tipo_unidade_id == 1

def test_atualizar(service):
    dto = UnidadeInputDTO(
        empreendimento_id=1,
        construtora_id=1,
        codigo_unidade="A101",
        metragem=75.5,
        valor=350000.00,
        observacoes="Unidade teste",
        tipo_unidade_id=1
    )

    criado = service.cadastrar(dto)

    atualizado_dto = UnidadeInputDTO(
        empreendimento_id=1,
        construtora_id=2,
        codigo_unidade="A102",
        metragem=80.0,
        valor=400000.00,
        observacoes="Atualizada",
        tipo_unidade_id=2   # <-- agora carrega 'Loja'
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.tipo_unidade_id == 2
    assert atualizado.codigo_unidade == "A102"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = UnidadeInputDTO(
        empreendimento_id=1,
        construtora_id=1,
        codigo_unidade="A103",
        metragem=60.0,
        valor=250000.00,
        observacoes="Para remover",
        tipo_unidade_id=3   # <-- agora carrega 'Residencial'
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
