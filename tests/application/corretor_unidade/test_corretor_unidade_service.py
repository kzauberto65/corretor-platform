import pytest
from src.application.corretor_unidade.services.corretor_unidade_service import CorretorUnidadeService
from src.infrastructure.corretor_unidade.repositories.corretor_unidade_repository import CorretorUnidadeRepository
from src.domain.corretor_unidade.dto.corretor_unidade_input_dto import CorretorUnidadeInputDTO


@pytest.fixture
def service():
    # Usa o banco REAL, sem apagar nada
    repo = CorretorUnidadeRepository()
    return CorretorUnidadeService(repo)


def test_cadastrar(service):
    dto = CorretorUnidadeInputDTO(
        corretor_id=310,
        unidade_id=410,
        tipo_vinculo="Responsável",
        observacoes="Teste inicial"
    )

    criado = service.cadastrar(dto)

    assert criado.corretor_id == 310
    assert criado.unidade_id == 410
    assert criado.tipo_vinculo == "Responsável"
    assert criado.observacoes == "Teste inicial"


def test_atualizar(service):
    dto = CorretorUnidadeInputDTO(
        corretor_id=320,
        unidade_id=420,
        tipo_vinculo="Auxiliar",
        observacoes="Teste"
    )

    service.cadastrar(dto)

    dto.tipo_vinculo = "Atualizado"
    dto.observacoes = "Nova observação"

    atualizado = service.atualizar(dto)

    assert atualizado.tipo_vinculo == "Atualizado"
    assert atualizado.observacoes == "Nova observação"


def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)


def test_buscar_por_ids(service):
    dto = CorretorUnidadeInputDTO(
        corretor_id=330,
        unidade_id=430,
        tipo_vinculo="Teste",
        observacoes="Busca"
    )

    service.cadastrar(dto)

    resultado = service.buscar_por_ids(330, 430)

    assert resultado is not None
    assert resultado.tipo_vinculo == "Teste"
    assert resultado.observacoes == "Busca"


def test_remover(service):
    dto = CorretorUnidadeInputDTO(
        corretor_id=340,
        unidade_id=440,
        tipo_vinculo="Remover",
        observacoes="Teste"
    )

    service.cadastrar(dto)

    removido = service.remover(340, 440)

    assert removido is True
