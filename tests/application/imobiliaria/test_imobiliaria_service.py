import pytest
from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.application.imobiliaria.services.imobiliaria_service import ImobiliariaService
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository

@pytest.fixture
def service():
    repo = ImobiliariaRepository()
    return ImobiliariaService(repo)

def test_cadastrar_e_buscar(service):
    dto = ImobiliariaInputDTO(
        nome="Imob Teste",
        cnpj="12.345.678/0001-99",
        contato="(11) 99999-9999",
        observacoes="Teste de integração"
    )
    criado = service.cadastrar(dto)
    assert criado.id is not None
    buscado = service.buscar_por_id(criado.id)
    assert buscado.nome == "Imob Teste"

def test_atualizar(service):
    dto = ImobiliariaInputDTO(
        nome="Imob Original",
        cnpj="00.000.000/0000-00",
        contato="(11) 88888-8888",
        observacoes="Original"
    )
    criado = service.cadastrar(dto)
    atualizado_dto = ImobiliariaInputDTO(
        nome="Imob Atualizada",
        cnpj="99.999.999/9999-99",
        contato="(11) 77777-7777",
        observacoes="Atualizado"
    )
    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.nome == "Imob Atualizada"

def test_consultar(service):
    results = service.consultar()
    assert isinstance(results, list)

def test_remover(service):
    dto = ImobiliariaInputDTO(
        nome="Imob Remover",
        cnpj="11.111.111/1111-11",
        contato="(11) 66666-6666",
        observacoes="Remover"
    )
    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)
    assert ok
    assert service.buscar_por_id(criado.id) is None
