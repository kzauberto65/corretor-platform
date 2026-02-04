import click
from src.application.unidade_referencia.services.unidade_referencia_service import UnidadeReferenciaService
from src.infrastructure.unidade_referencia.repositories.unidade_referencia_repository import UnidadeReferenciaRepository
from src.domain.unidade_referencia.dto.unidade_referencia_input_dto import UnidadeReferenciaInputDTO

repo = UnidadeReferenciaRepository()
service = UnidadeReferenciaService(repo)

@click.group()
def unidade_referencia():
    """Gerenciamento de Unidades de Referência"""
    pass

@click.command()
@click.option("--codigo", required=True)
def cadastrar(codigo):
    dto = UnidadeReferenciaInputDTO(codigo=codigo)
    criado = service.cadastrar(dto)
    click.echo(f"Unidade de referência cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--codigo", required=True)
def atualizar(id, codigo):
    dto = UnidadeReferenciaInputDTO(codigo=codigo)
    atualizado = service.atualizar(id, dto)
    click.echo(f"Unidade de referência {atualizado.id} atualizada com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.codigo}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Unidade de referência não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Unidade de referência removida com sucesso")
    else:
        click.echo("Falha ao remover")

unidade_referencia.add_command(cadastrar)
unidade_referencia.add_command(atualizar)
unidade_referencia.add_command(consultar)
unidade_referencia.add_command(buscar)
unidade_referencia.add_command(remover)
