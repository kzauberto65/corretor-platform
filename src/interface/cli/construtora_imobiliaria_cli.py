import click
from src.application.construtora_imobiliaria.services.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO

repo = ConstrutoraImobiliariaRepository()
service = ConstrutoraImobiliariaService(repo)

@click.group()
def construtora_imobiliaria():
    """Gerenciamento de Construtora-Imobiliária"""
    pass

@click.command()
@click.option("--construtora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--tipo_parceria", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def cadastrar(construtora_id, imobiliaria_id, tipo_parceria, observacoes):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=construtora_id,
        imobiliaria_id=imobiliaria_id,
        tipo_parceria=tipo_parceria,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"Relacionamento cadastrado: Construtora {criado.construtora_id} ↔ Imobiliária {criado.imobiliaria_id}")

@click.command()
@click.option("--construtora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--tipo_parceria", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def atualizar(construtora_id, imobiliaria_id, tipo_parceria, observacoes):
    dto = ConstrutoraImobiliariaInputDTO(
        construtora_id=construtora_id,
        imobiliaria_id=imobiliaria_id,
        tipo_parceria=tipo_parceria,
        observacoes=observacoes
    )
    atualizado = service.atualizar(dto)
    click.echo(f"Relacionamento atualizado: Construtora {atualizado.construtora_id} ↔ Imobiliária {atualizado.imobiliaria_id}")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.construtora_id} ↔ {item.imobiliaria_id} | Parceria: {item.tipo_parceria}")

@click.command()
@click.option("--construtora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def buscar(construtora_id, imobiliaria_id):
    encontrado = service.buscar_por_ids(construtora_id, imobiliaria_id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Relacionamento não encontrado")

@click.command()
@click.option("--construtora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def remover(construtora_id, imobiliaria_id):
    ok = service.remover(construtora_id, imobiliaria_id)
    if ok:
        click.echo("Relacionamento removido com sucesso")
    else:
        click.echo("Falha ao remover")

construtora_imobiliaria.add_command(cadastrar)
construtora_imobiliaria.add_command(atualizar)
construtora_imobiliaria.add_command(consultar)
construtora_imobiliaria.add_command(buscar)
construtora_imobiliaria.add_command(remover)
