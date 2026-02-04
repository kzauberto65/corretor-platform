import click
from src.application.corretor_unidade.services.corretor_unidade_service import CorretorUnidadeService
from src.infrastructure.corretor_unidade.repositories.corretor_unidade_repository import CorretorUnidadeRepository
from src.domain.corretor_unidade.dto.corretor_unidade_input_dto import CorretorUnidadeInputDTO

repo = CorretorUnidadeRepository()
service = CorretorUnidadeService(repo)

@click.group()
def corretor_unidade():
    """Gerenciamento de Corretor-Unidade"""
    pass

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--unidade_id", required=True, type=int)
@click.option("--tipo_vinculo", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def cadastrar(corretor_id, unidade_id, tipo_vinculo, observacoes):
    dto = CorretorUnidadeInputDTO(
        corretor_id=corretor_id,
        unidade_id=unidade_id,
        tipo_vinculo=tipo_vinculo,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"Relacionamento cadastrado: Corretor {criado.corretor_id} ↔ Unidade {criado.unidade_id}")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--unidade_id", required=True, type=int)
@click.option("--tipo_vinculo", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def atualizar(corretor_id, unidade_id, tipo_vinculo, observacoes):
    dto = CorretorUnidadeInputDTO(
        corretor_id=corretor_id,
        unidade_id=unidade_id,
        tipo_vinculo=tipo_vinculo,
        observacoes=observacoes
    )
    atualizado = service.atualizar(dto)
    click.echo(f"Relacionamento atualizado: Corretor {atualizado.corretor_id} ↔ Unidade {atualizado.unidade_id}")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.corretor_id} ↔ {item.unidade_id} | Vínculo: {item.tipo_vinculo}")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--unidade_id", required=True, type=int)
def buscar(corretor_id, unidade_id):
    encontrado = service.buscar_por_ids(corretor_id, unidade_id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Relacionamento não encontrado")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--unidade_id", required=True, type=int)
def remover(corretor_id, unidade_id):
    ok = service.remover(corretor_id, unidade_id)
    if ok:
        click.echo("Relacionamento removido com sucesso")
    else:
        click.echo("Falha ao remover")

corretor_unidade.add_command(cadastrar)
corretor_unidade.add_command(atualizar)
corretor_unidade.add_command(consultar)
corretor_unidade.add_command(buscar)
corretor_unidade.add_command(remover)
