import click
from src.application.unidade_referencia_tipo.services.unidade_referencia_tipo_service import UnidadeReferenciaTipoService
from src.infrastructure.unidade_referencia_tipo.repositories.unidade_referencia_tipo_repository import UnidadeReferenciaTipoRepository
from src.domain.unidade_referencia_tipo.dto.unidade_referencia_tipo_input_dto import UnidadeReferenciaTipoInputDTO

repo = UnidadeReferenciaTipoRepository()
service = UnidadeReferenciaTipoService(repo)

@click.group()
def unidade_referencia_tipo():
    """Gerenciamento de Tipos de Unidade de Referência"""
    pass

@click.command()
@click.option("--nome", required=True)
def cadastrar(nome):
    dto = UnidadeReferenciaTipoInputDTO(nome=nome)
    criado = service.cadastrar(dto)
    click.echo(f"Tipo cadastrado com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=True)
def atualizar(id, nome):
    dto = UnidadeReferenciaTipoInputDTO(nome=nome)
    atualizado = service.atualizar(id, dto)
    click.echo(f"Tipo {atualizado.id} atualizado com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.nome}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Tipo não encontrado")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Tipo removido com sucesso")
    else:
        click.echo("Falha ao remover")

unidade_referencia_tipo.add_command(cadastrar)
unidade_referencia_tipo.add_command(atualizar)
unidade_referencia_tipo.add_command(consultar)
unidade_referencia_tipo.add_command(buscar)
unidade_referencia_tipo.add_command(remover)
