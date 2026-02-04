import pytest
from src.application.spe.services.spe_service import SPEService
from src.infrastructure.spe.repositories.spe_repository import SPERepository
from src.domain.spe.dto.spe_input_dto import SPEInputDTO

@pytest.fixture
def service():
    repo = SPERepository()
    return SPEService(repo)

def test_cadastrar(service):
    dto = SPEInputDTO(
        nome="SPE Alpha",
        cnpj="12.345.678/0001-99",
        observacoes="Primeira SPE de teste"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "SPE Alpha"

def test_atualizar(service):
    dto = SPEInputDTO(
        nome="SPE Alpha",
        cnpj="12.345.678/0001-99",
        observacoes="Primeira SPE de teste"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = SPEInputDTO(
        nome="SPE Beta",
        cnpj="98.765.432/0001-11",
        observacoes="Atualizada com sucesso"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "SPE Beta"
    assert atualizado.cnpj == "98.765.432/0001-11"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = SPEInputDTO(
        nome="SPE Gamma",
        cnpj="11.222.333/0001-44",
        observacoes="SPE temporária"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
