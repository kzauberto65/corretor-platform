import pytest
from src.application.unidade_referencia.services.unidade_referencia_service import UnidadeReferenciaService
from src.infrastructure.unidade_referencia.repositories.unidade_referencia_repository import UnidadeReferenciaRepository
from src.domain.unidade_referencia.dto.unidade_referencia_input_dto import UnidadeReferenciaInputDTO

@pytest.fixture
def service():
    repo = UnidadeReferenciaRepository()
    return UnidadeReferenciaService(repo)

def test_cadastrar(service):
    dto = UnidadeReferenciaInputDTO(
        codigo="REF-001"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.codigo == "REF-001"

def test_atualizar(service):
    dto = UnidadeReferenciaInputDTO(
        codigo="REF-001"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = UnidadeReferenciaInputDTO(
        codigo="REF-002"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.codigo == "REF-002"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = UnidadeReferenciaInputDTO(
        codigo="REF-003"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
