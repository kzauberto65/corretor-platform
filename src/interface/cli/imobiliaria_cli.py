import click
from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO
from src.application.imobiliaria.services.imobiliaria_service import ImobiliariaService
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository

repo = ImobiliariaRepository()
service = ImobiliariaService(repo)

@click.group()
def imobiliaria():
    pass

@imobiliaria.command()
@click.option("--nome", required=True)
@click.option("--cnpj")
@click.option("--contato")
@click.option("--observacoes")
def cadastrar(nome, cnpj, contato, observacoes):
    dto = ImobiliariaInputDTO(nome=nome, cnpj=cnpj, contato=contato, observacoes=observacoes)
    result = service.cadastrar(dto)
    click.echo(f"Imobiliária cadastrada com ID {result.id}")

@imobiliaria.command()
@click.argument("id", type=int)
@click.option("--nome")
@click.option("--cnpj")
@click.option("--contato")
@click.option("--observacoes")
def atualizar(id, nome, cnpj, contato, observacoes):
    dto = ImobiliariaInputDTO(nome=nome, cnpj=cnpj, contato=contato, observacoes=observacoes)
    result = service.atualizar(id, dto)
    if result:
        click.echo(f"Imobiliária {id} atualizada.")
    else:
        click.echo("Imobiliária não encontrada.")

@imobiliaria.command()
def consultar():
    results = service.consultar()
    for r in results:
        click.echo(f"{r.id} - {r.nome} - {r.cnpj}")

@imobiliaria.command()
@click.argument("id", type=int)
def buscar(id):
    result = service.buscar_por_id(id)
    if result:
        click.echo(result)
    else:
        click.echo("Imobiliária não encontrada.")

@imobiliaria.command()
@click.argument("id", type=int)
def remover(id):
    service.remover(id)
    click.echo(f"Imobiliária {id} removida.")

if __name__ == "__main__":
    imobiliaria()
