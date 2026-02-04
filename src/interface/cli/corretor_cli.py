import click
from src.application.corretor.services.corretor_service import CorretorService
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO

repo = CorretorRepository()
service = CorretorService(repo)

@click.group()
def corretor():
    """Gerenciamento de corretores"""
    pass

@click.command()
@click.option("--nome", required=False)
@click.option("--telefone", required=False)
@click.option("--email", required=False)
@click.option("--creci", required=False)
@click.option("--observacoes", required=False)
def cadastrar(nome, telefone, email, creci, observacoes):
    dto = CorretorInputDTO(
        nome=nome,
        telefone=telefone,
        email=email,
        creci=creci,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"Corretor cadastrado com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=False)
@click.option("--telefone", required=False)
@click.option("--email", required=False)
@click.option("--creci", required=False)
@click.option("--observacoes", required=False)
def atualizar(id, nome, telefone, email, creci, observacoes):
    dto = CorretorInputDTO(
        nome=nome,
        telefone=telefone,
        email=email,
        creci=creci,
        observacoes=observacoes
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Corretor {atualizado.id} atualizado com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.nome} - {item.telefone}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Corretor não encontrado")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Corretor removido com sucesso")
    else:
        click.echo("Falha ao remover")

corretor.add_command(cadastrar)
corretor.add_command(atualizar)
corretor.add_command(consultar)
corretor.add_command(buscar)
corretor.add_command(remover)
