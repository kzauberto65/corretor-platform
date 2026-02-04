import click
from src.application.corretor_imobiliaria.services.corretor_imobiliaria_service import CorretorImobiliariaService
from src.infrastructure.corretor_imobiliaria.repositories.corretor_imobiliaria_repository import CorretorImobiliariaRepository
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO

repo = CorretorImobiliariaRepository()
service = CorretorImobiliariaService(repo)

@click.group()
def corretor_imobiliaria():
    """Gerenciamento de Corretor-Imobiliária"""
    pass

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--tipo_vinculo", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def cadastrar(corretor_id, imobiliaria_id, tipo_vinculo, observacoes):
    dto = CorretorImobiliariaInputDTO(
        corretor_id=corretor_id,
        imobiliaria_id=imobiliaria_id,
        tipo_vinculo=tipo_vinculo,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"Relacionamento cadastrado: Corretor {criado.corretor_id} ↔ Imobiliária {criado.imobiliaria_id}")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--tipo_vinculo", required=False, type=str)
@click.option("--observacoes", required=False, type=str)
def atualizar(corretor_id, imobiliaria_id, tipo_vinculo, observacoes):
    dto = CorretorImobiliariaInputDTO(
        corretor_id=corretor_id,
        imobiliaria_id=imobiliaria_id,
        tipo_vinculo=tipo_vinculo,
        observacoes=observacoes
    )
    atualizado = service.atualizar(dto)
    click.echo(f"Relacionamento atualizado: Corretor {atualizado.corretor_id} ↔ Imobiliária {atualizado.imobiliaria_id}")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.corretor_id} ↔ {item.imobiliaria_id} | Vínculo: {item.tipo_vinculo}")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def buscar(corretor_id, imobiliaria_id):
    encontrado = service.buscar_por_ids(corretor_id, imobiliaria_id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Relacionamento não encontrado")

@click.command()
@click.option("--corretor_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def remover(corretor_id, imobiliaria_id):
    ok = service.remover(corretor_id, imobiliaria_id)
    if ok:
        click.echo("Relacionamento removido com sucesso")
    else:
        click.echo("Falha ao remover")

corretor_imobiliaria.add_command(cadastrar)
corretor_imobiliaria.add_command(atualizar)
corretor_imobiliaria.add_command(consultar)
corretor_imobiliaria.add_command(buscar)
corretor_imobiliaria.add_command(remover)
