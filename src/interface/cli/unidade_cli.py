import click
from src.application.unidade.services.unidade_service import UnidadeService
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository
from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO

repo = UnidadeRepository()
service = UnidadeService(repo)

@click.group()
def unidade():
    """Gerenciamento de Unidades"""
    pass

@click.command()
@click.option("--empreendimento_id", required=True, type=int)
@click.option("--construtora_id", required=False, type=int)
@click.option("--codigo_unidade", required=False, type=str)
@click.option("--metragem", required=False, type=float)
@click.option("--valor", required=False, type=float)
@click.option("--observacoes", required=False, type=str)
@click.option("--tipo_unidade_id", required=False, type=int)
def cadastrar(empreendimento_id, construtora_id, codigo_unidade, metragem, valor, observacoes, tipo_unidade_id):
    dto = UnidadeInputDTO(
        empreendimento_id=empreendimento_id,
        construtora_id=construtora_id,
        codigo_unidade=codigo_unidade,
        metragem=metragem,
        valor=valor,
        observacoes=observacoes,
        tipo_unidade_id=tipo_unidade_id
    )
    criado = service.cadastrar(dto)
    click.echo(f"Unidade cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--empreendimento_id", required=True, type=int)
@click.option("--construtora_id", required=False, type=int)
@click.option("--codigo_unidade", required=False, type=str)
@click.option("--metragem", required=False, type=float)
@click.option("--valor", required=False, type=float)
@click.option("--observacoes", required=False, type=str)
@click.option("--tipo_unidade_id", required=False, type=int)
def atualizar(id, empreendimento_id, construtora_id, codigo_unidade, metragem, valor, observacoes, tipo_unidade_id):
    dto = UnidadeInputDTO(
        empreendimento_id=empreendimento_id,
        construtora_id=construtora_id,
        codigo_unidade=codigo_unidade,
        metragem=metragem,
        valor=valor,
        observacoes=observacoes,
        tipo_unidade_id=tipo_unidade_id
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Unidade {atualizado.id} atualizada com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - Empreendimento {item.empreendimento_id} - Código {item.codigo_unidade}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Unidade não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Unidade removida com sucesso")
    else:
        click.echo("Falha ao remover")

unidade.add_command(cadastrar)
unidade.add_command(atualizar)
unidade.add_command(consultar)
unidade.add_command(buscar)
unidade.add_command(remover)
