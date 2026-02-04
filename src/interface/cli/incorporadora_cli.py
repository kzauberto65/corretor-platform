import click
from src.application.incorporadora.services.incorporadora_service import IncorporadoraService
from src.infrastructure.incorporadora.repositories.incorporadora_repository import IncorporadoraRepository
from src.domain.incorporadora.dto.incorporadora_input_dto import IncorporadoraInputDTO

repo = IncorporadoraRepository()
service = IncorporadoraService(repo)

@click.group()
def incorporadora():
    """Gerenciamento de incorporadoras"""
    pass

@click.command()
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--reputacao", type=int, required=False)
@click.option("--historico_obra", required=False)
def cadastrar(nome, cnpj, reputacao, historico_obra):
    dto = IncorporadoraInputDTO(
        nome=nome,
        cnpj=cnpj,
        reputacao=reputacao,
        historico_obra=historico_obra
    )
    criado = service.cadastrar(dto)
    click.echo(f"Incorporadora cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--reputacao", type=int, required=False)
@click.option("--historico_obra", required=False)
def atualizar(id, nome, cnpj, reputacao, historico_obra):
    dto = IncorporadoraInputDTO(
        nome=nome,
        cnpj=cnpj,
        reputacao=reputacao,
        historico_obra=historico_obra
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Incorporadora {atualizado.id} atualizada com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.nome} - {item.cnpj}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Incorporadora não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Incorporadora removida com sucesso")
    else:
        click.echo("Falha ao remover")

incorporadora.add_command(cadastrar)
incorporadora.add_command(atualizar)
incorporadora.add_command(consultar)
incorporadora.add_command(buscar)
incorporadora.add_command(remover)
