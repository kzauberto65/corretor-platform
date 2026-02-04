import pytest
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO

@pytest.fixture
def service():
    repo = EmpreendimentoRepository()
    return EmpreendimentoService(repo)

def test_cadastrar(service):
    dto = EmpreendimentoInputDTO(
        regiao="Sul",
        bairro="Centro",
        cidade="Curitiba",
        estado="PR",
        produto="Residencial",
        endereco="Rua Teste, 123",
        data_entrega="2025-12-01",
        status_entrega="Em Obras",
        tipo="Apartamento",
        descricao="Teste",
        preco=350000.00,
        proprietario_id=None,
        incorporadora_id=None,
        unidade_referencia_id=None,
        spe_id=None,
        periodo_lancamento="2024",
        nome="Residencial Teste",
        tipologia="2 Dorms"
    )

    criado = service.cadastrar(dto)
    assert criado.id is not None
    assert criado.nome == "Residencial Teste"

def test_atualizar(service):
    dto = EmpreendimentoInputDTO(
        regiao="Sul",
        bairro="Centro",
        cidade="Curitiba",
        estado="PR",
        produto="Residencial",
        endereco="Rua Teste, 123",
        data_entrega="2025-12-01",
        status_entrega="Em Obras",
        tipo="Apartamento",
        descricao="Teste",
        preco=350000.00,
        proprietario_id=None,
        incorporadora_id=None,
        unidade_referencia_id=None,
        spe_id=None,
        periodo_lancamento="2024",
        nome="Residencial Teste",
        tipologia="2 Dorms"
    )

    criado = service.cadastrar(dto)

    atualizado = EmpreendimentoInputDTO(
        regiao="Sul",
        bairro="Centro",
        cidade="Curitiba",
        estado="PR",
        produto="Residencial",
        endereco="Rua Teste, 123",
        data_entrega="2025-12-01",
        status_entrega="Concluído",
        tipo="Apartamento",
        descricao="Atualizado",
        preco=360000.00,
        proprietario_id=None,
        incorporadora_id=None,
        unidade_referencia_id=None,
        spe_id=None,
        periodo_lancamento="2024",
        nome="Residencial Atualizado",
        tipologia="2 Dorms"
    )

    result = service.atualizar(criado.id, atualizado)
    assert result.nome == "Residencial Atualizado"

def test_consultar(service):
    lista = service.consultar()
    assert isinstance(lista, list)

def test_remover(service):
    dto = EmpreendimentoInputDTO(
        regiao="Sul",
        bairro="Centro",
        cidade="Curitiba",
        estado="PR",
        produto="Residencial",
        endereco="Rua Teste, 123",
        data_entrega="2025-12-01",
        status_entrega="Em Obras",
        tipo="Apartamento",
        descricao="Teste",
        preco=350000.00,
        proprietario_id=None,
        incorporadora_id=None,
        unidade_referencia_id=None,
        spe_id=None,
        periodo_lancamento="2024",
        nome="Residencial Remover",
        tipologia="2 Dorms"
    )

    criado = service.cadastrar(dto)
    ok = service.remover(criado.id)

    assert ok
    assert service.buscar_por_id(criado.id) is None
