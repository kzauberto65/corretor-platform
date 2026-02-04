import pytest
from src.application.incorporadora_imobiliaria.services.incorporadora_imobiliaria_service import IncorporadoraImobiliariaService
from src.infrastructure.incorporadora_imobiliaria.repositories.incorporadora_imobiliaria_repository import IncorporadoraImobiliariaRepository
from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_input_dto import IncorporadoraImobiliariaInputDTO

@pytest.fixture
def service():
    repo = IncorporadoraImobiliariaRepository()
    return IncorporadoraImobiliariaService(repo)

# ---------------------------------------------------------
# Teste: cadastrar
# ---------------------------------------------------------
def test_cadastrar(service):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=1,
        imobiliaria_id=2,
        observacoes="Teste de cadastro"
    )

    criado = service.cadastrar(dto)

    assert criado.incorporadora_id == 1
    assert criado.imobiliaria_id == 2
    assert criado.observacoes == "Teste de cadastro"

# ---------------------------------------------------------
# Teste: atualizar
# ---------------------------------------------------------
def test_atualizar(service):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=3,
        imobiliaria_id=4,
        observacoes="Antes"
    )

    service.cadastrar(dto)

    dto_atualizado = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=3,
        imobiliaria_id=4,
        observacoes="Depois"
    )

    atualizado = service.atualizar(dto_atualizado)

    assert atualizado.observacoes == "Depois"

# ---------------------------------------------------------
# Teste: consultar
# ---------------------------------------------------------
def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

# ---------------------------------------------------------
# Teste: buscar por IDs
# ---------------------------------------------------------
def test_buscar_por_ids(service):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=5,
        imobiliaria_id=6,
        observacoes="Busca"
    )

    service.cadastrar(dto)

    resultado = service.buscar_por_ids(5, 6)

    assert resultado is not None
    assert resultado.incorporadora_id == 5
    assert resultado.imobiliaria_id == 6
    assert resultado.observacoes == "Busca"

# ---------------------------------------------------------
# Teste: remover
# ---------------------------------------------------------
def test_remover(service):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=7,
        imobiliaria_id=8,
        observacoes="Remover"
    )

    service.cadastrar(dto)

    removido = service.remover(7, 8)

    assert removido is True
