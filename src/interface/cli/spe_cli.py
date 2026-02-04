import click
from src.application.spe.services.spe_service import SPEService
from src.infrastructure.spe.repositories.spe_repository import SPERepository
from src.domain.spe.dto.spe_input_dto import SPEInputDTO

repo = SPERepository()
service = SPEService(repo)

@click.group()
def spe():
    """Gerenciamento de SPEs"""
    pass

@click.command()
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--observacoes", required=False)
def cadastrar(nome, cnpj, observacoes):
    dto = SPEInputDTO(
        nome=nome,
        cnpj=cnpj,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"SPE cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--observacoes", required=False)
def atualizar(id, nome, cnpj, observacoes):
    dto = SPEInputDTO(
        nome=nome,
        cnpj=cnpj,
        observacoes=observacoes
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"SPE {atualizado.id} atualizada com sucesso")

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
        click.echo("SPE não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("SPE removida com sucesso")
    else:
        click.echo("Falha ao remover")

spe.add_command(cadastrar)
spe.add_command(atualizar)
spe.add_command(consultar)
spe.add_command(buscar)
spe.add_command(remover)
