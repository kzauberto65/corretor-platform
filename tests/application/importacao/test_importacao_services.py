import pytest
from src.application.importacao.services.importacao_service import ImportacaoService
from src.infrastructure.importacao.repositories.importacao_repository import ImportacaoRepository
from src.domain.importacao.dto.importacao_input_dto import ImportacaoInputDTO

@pytest.fixture
def service():
    repo = ImportacaoRepository()
    return ImportacaoService(repo)

def test_cadastrar(service):
    dto = ImportacaoInputDTO(
        tipo="CSV",
        arquivo="dados.csv",
        origem="sistema_x",
        total_registros=100,
        status="pendente",
        data_execucao="2024-01-01 10:00:00",
        sucesso=0,
        erros=0,
        log="Iniciando importação"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.tipo == "CSV"

def test_atualizar(service):
    dto = ImportacaoInputDTO(
        tipo="CSV",
        arquivo="dados.csv",
        origem="sistema_x",
        total_registros=100,
        status="pendente",
        data_execucao="2024-01-01 10:00:00",
        sucesso=0,
        erros=0,
        log="Iniciando importação"
    )

    criado = service.cadastrar(dto)

    atualizado_dto = ImportacaoInputDTO(
        tipo="JSON",
        arquivo="dados.json",
        origem="sistema_y",
        total_registros=200,
        status="concluida",
        data_execucao="2024-01-02 12:00:00",
        sucesso=200,
        erros=0,
        log="Processo finalizado"
    )

    atualizado = service.atualizar(criado.id, atualizado_dto)
    assert atualizado.tipo == "JSON"
    assert atualizado.status == "concluida"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = ImportacaoInputDTO(
        tipo="XML",
        arquivo="dados.xml",
        origem="sistema_z",
        total_registros=50,
        status="pendente",
        data_execucao="2024-01-03 09:00:00",
        sucesso=0,
        erros=0,
        log="Preparando importação"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
