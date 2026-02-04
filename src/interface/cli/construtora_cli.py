import click
from src.application.construtora.services.construtora_service import ConstrutoraService
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO

repo = ConstrutoraRepository()
service = ConstrutoraService(repo)

@click.group()
def construtora():
    """Gerenciamento de construtoras"""
    pass

@click.command()
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--contato", required=False)
@click.option("--observacoes", required=False)
@click.option("--fonte", required=False)
@click.option("--data_registro", required=False)
@click.option("--usuario_id", required=False)
@click.option("--justificativa", required=False)
def cadastrar(nome, cnpj, contato, observacoes, fonte, data_registro, usuario_id, justificativa):
    dto = ConstrutoraInputDTO(
        nome=nome,
        cnpj=cnpj,
        contato=contato,
        observacoes=observacoes,
        fonte=fonte,
        data_registro=data_registro,
        usuario_id=usuario_id,
        justificativa=justificativa
    )
    criado = service.cadastrar(dto)
    click.echo(f"Construtora cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=False)
@click.option("--cnpj", required=False)
@click.option("--contato", required=False)
@click.option("--observacoes", required=False)
@click.option("--fonte", required=False)
@click.option("--data_registro", required=False)
@click.option("--usuario_id", required=False)
@click.option("--justificativa", required=False)
def atualizar(id, nome, cnpj, contato, observacoes, fonte, data_registro, usuario_id, justificativa):
    dto = ConstrutoraInputDTO(
        nome=nome,
        cnpj=cnpj,
        contato=contato,
        observacoes=observacoes,
        fonte=fonte,
        data_registro=data_registro,
        usuario_id=usuario_id,
        justificativa=justificativa
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Construtora {atualizado.id} atualizada com sucesso")

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
        click.echo("Construtora não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Construtora removida com sucesso")
    else:
        click.echo("Falha ao remover")

construtora.add_command(cadastrar)
construtora.add_command(atualizar)
construtora.add_command(consultar)
construtora.add_command(buscar)
construtora.add_command(remover)
