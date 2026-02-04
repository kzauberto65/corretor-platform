import pytest
from src.application.unidade_referencia_tipo.services.unidade_referencia_tipo_service import UnidadeReferenciaTipoService
from src.infrastructure.unidade_referencia_tipo.repositories.unidade_referencia_tipo_repository import UnidadeReferenciaTipoRepository
from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_input_dto import UnidadeReferenciaTipoInputDTO

@pytest.fixture
def service():
    repo = UnidadeReferenciaTipoRepository()
    return UnidadeReferenciaTipoService(repo)

def test_cadastrar(service):
    dto = UnidadeReferenciaTipoInputDTO(
        nome="Residencial"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "Residencial"

def test_atualizar(service):
    dto = UnidadeReferenciaTipoInputDTO(
        nome="Residencial"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = UnidadeReferenciaTipoInputDTO(
        nome="Comercial"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "Comercial"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = UnidadeReferenciaTipoInputDTO(
        nome="Temporário"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
