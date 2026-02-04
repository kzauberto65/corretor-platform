import pytest
from src.application.construtora_imobiliaria.services.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO


@pytest.fixture
def service():
    # Usa o banco REAL, sem apagar nada
    repo = ConstrutoraImobiliariaRepository()
    return ConstrutoraImobiliariaService(repo)


def test_cadastrar(service):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=10,
        imobiliaria_id=20,
        tipo_parceria="Exclusiva",
        observacoes="Teste inicial"
    )

    criado = service.cadastrar(dto)

    assert criado.construtora_id == 10
    assert criado.imobiliaria_id == 20
    assert criado.tipo_parceria == "Exclusiva"
    assert criado.observacoes == "Teste inicial"


def test_atualizar(service):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=11,
        imobiliaria_id=21,
        tipo_parceria="Parcial",
        observacoes="Teste"
    )

    service.cadastrar(dto)

    dto.tipo_parceria = "Atualizada"
    dto.observacoes = "Nova observação"

    atualizado = service.atualizar(dto)

    assert atualizado.tipo_parceria == "Atualizada"
    assert atualizado.observacoes == "Nova observação"


def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)


def test_buscar_por_ids(service):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=12,
        imobiliaria_id=22,
        tipo_parceria="Teste",
        observacoes="Busca"
    )

    service.cadastrar(dto)

    resultado = service.buscar_por_ids(12, 22)

    assert resultado is not None
    assert resultado.tipo_parceria == "Teste"
    assert resultado.observacoes == "Busca"


def test_remover(service):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=13,
        imobiliaria_id=23,
        tipo_parceria="Remover",
        observacoes="Teste"
    )

    service.cadastrar(dto)

    removido = service.remover(13, 23)

    assert removido is True
