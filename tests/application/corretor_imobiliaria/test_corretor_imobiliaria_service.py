import pytest
from src.application.corretor_imobiliaria.services.corretor_imobiliaria_service import CorretorImobiliariaService
from src.infrastructure.corretor_imobiliaria.repositories.corretor_imobiliaria_repository import CorretorImobiliariaRepository
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO


@pytest.fixture
def service():
    # Usa o banco REAL, sem apagar nada
    repo = CorretorImobiliariaRepository()
    return CorretorImobiliariaService(repo)


def test_cadastrar(service):
    dto = CorretorImobiliariaInputDTO(
        corretor_id=110,
        imobiliaria_id=210,
        tipo_vinculo="Exclusivo",
        observacoes="Teste inicial"
    )

    criado = service.cadastrar(dto)

    assert criado.corretor_id == 110
    assert criado.imobiliaria_id == 210
    assert criado.tipo_vinculo == "Exclusivo"
    assert criado.observacoes == "Teste inicial"


def test_atualizar(service):
    dto = CorretorImobiliariaInputDTO(
        corretor_id=120,
        imobiliaria_id=220,
        tipo_vinculo="Parcial",
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
    dto = CorretorImobiliariaInputDTO(
        corretor_id=130,
        imobiliaria_id=230,
        tipo_vinculo="Teste",
        observacoes="Busca"
    )

    service.cadastrar(dto)

    resultado = service.buscar_por_ids(130, 230)

    assert resultado is not None
    assert resultado.tipo_vinculo == "Teste"
    assert resultado.observacoes == "Busca"


def test_remover(service):
    dto = CorretorImobiliariaInputDTO(
        corretor_id=140,
        imobiliaria_id=240,
        tipo_vinculo="Remover",
        observacoes="Teste"
    )

    service.cadastrar(dto)

    removido = service.remover(140, 240)

    assert removido is True
