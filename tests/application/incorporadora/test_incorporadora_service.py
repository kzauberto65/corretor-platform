import pytest
from src.application.incorporadora.services.incorporadora_service import IncorporadoraService
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository
from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO

@pytest.fixture
def service():
    repo = IncorporadoraRepository()
    return IncorporadoraService(repo)

def test_cadastrar(service):
    dto = IncorporadoraInputDTO(
        nome="Incorporadora Alfa",
        cnpj="12.345.678/0001-99",
        reputacao=8,
        historico_obra="Obras entregues no prazo"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "Incorporadora Alfa"

def test_atualizar(service):
    dto = IncorporadoraInputDTO(
        nome="Incorporadora Alfa",
        cnpj="12.345.678/0001-99",
        reputacao=8,
        historico_obra="Obras entregues no prazo"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = IncorporadoraInputDTO(
        nome="Incorporadora Beta",
        cnpj="98.765.432/0001-11",
        reputacao=9,
        historico_obra="Histórico excelente"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "Incorporadora Beta"
    assert atualizado.reputacao == 9

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = IncorporadoraInputDTO(
        nome="Incorporadora Gama",
        cnpj="11.222.333/0001-44",
        reputacao=7,
        historico_obra="Boa reputação"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
