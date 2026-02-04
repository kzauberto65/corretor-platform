import pytest
from src.application.corretor.services.corretor_service import CorretorService
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO

@pytest.fixture
def service():
    repo = CorretorRepository()
    return CorretorService(repo)

def test_cadastrar(service):
    dto = CorretorInputDTO(
        nome="Corretor Teste",
        telefone="11999999999",
        email="teste@corretor.com",
        creci="12345-F",
        observacoes="Observação teste"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "Corretor Teste"

def test_atualizar(service):
    dto = CorretorInputDTO(
        nome="Corretor Teste",
        telefone="11999999999",
        email="teste@corretor.com",
        creci="12345-F",
        observacoes="Observação teste"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = CorretorInputDTO(
        nome="Corretor Atualizado",
        telefone="11888888888",
        email="novo@corretor.com",
        creci="54321-F",
        observacoes="Atualizado"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "Corretor Atualizado"
    assert atualizado.telefone == "11888888888"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = CorretorInputDTO(
        nome="Corretor Remover",
        telefone="11777777777",
        email="remover@corretor.com",
        creci="99999-F",
        observacoes="Teste remover"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
