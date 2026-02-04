import pytest
from src.application.construtora.services.construtora_service import ConstrutoraService
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO

@pytest.fixture
def service():
    repo = ConstrutoraRepository()
    return ConstrutoraService(repo)

def test_cadastrar(service):
    dto = ConstrutoraInputDTO(
        nome="Construtora Teste",
        cnpj="00.000.000/0000-00",
        contato="contato@teste.com",
        observacoes="Observação teste",
        fonte="Site",
        data_registro="2025-01-01",
        usuario_id="1",
        justificativa="Cadastro inicial"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "Construtora Teste"

def test_atualizar(service):
    dto = ConstrutoraInputDTO(
        nome="Construtora Teste",
        cnpj="00.000.000/0000-00",
        contato="contato@teste.com",
        observacoes="Observação teste",
        fonte="Site",
        data_registro="2025-01-01",
        usuario_id="1",
        justificativa="Cadastro inicial"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = ConstrutoraInputDTO(
        nome="Construtora Atualizada",
        cnpj="11.111.111/1111-11",
        contato="novo@teste.com",
        observacoes="Atualizado",
        fonte="Atualizado",
        data_registro="2025-02-01",
        usuario_id="2",
        justificativa="Atualização"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "Construtora Atualizada"
    assert atualizado.cnpj == "11.111.111/1111-11"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = ConstrutoraInputDTO(
        nome="Construtora Remover",
        cnpj="22.222.222/2222-22",
        contato="remover@teste.com",
        observacoes="Teste remover",
        fonte="Fonte",
        data_registro="2025-03-01",
        usuario_id="3",
        justificativa="Remoção"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
