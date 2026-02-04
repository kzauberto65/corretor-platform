import click
from src.application.importacao.services.importacao_service import ImportacaoService
from src.infrastructure.importacao.repositories.importacao_repository import ImportacaoRepository
from src.domain.importacao.dto.importacao_input_dto import ImportacaoInputDTO

repo = ImportacaoRepository()
service = ImportacaoService(repo)

@click.group()
def importacao():
    """Gerenciamento de importações"""
    pass

@click.command()
@click.option("--tipo", required=False)
@click.option("--arquivo", required=False)
@click.option("--origem", required=False)
@click.option("--total_registros", type=int, required=False)
@click.option("--status", required=False)
@click.option("--data_execucao", required=False)
@click.option("--sucesso", type=int, required=False)
@click.option("--erros", type=int, required=False)
@click.option("--log", required=False)
def cadastrar(tipo, arquivo, origem, total_registros, status, data_execucao, sucesso, erros, log):
    dto = ImportacaoInputDTO(
        tipo=tipo,
        arquivo=arquivo,
        origem=origem,
        total_registros=total_registros,
        status=status,
        data_execucao=data_execucao,
        sucesso=sucesso,
        erros=erros,
        log=log
    )
    criado = service.cadastrar(dto)
    click.echo(f"Importação cadastrada com ID {criado.id}")

@click.command()
@click.argument("id", type=int)
@click.option("--tipo", required=False)
@click.option("--arquivo", required=False)
@click.option("--origem", required=False)
@click.option("--total_registros", type=int, required=False)
@click.option("--status", required=False)
@click.option("--data_execucao", required=False)
@click.option("--sucesso", type=int, required=False)
@click.option("--erros", type=int, required=False)
@click.option("--log", required=False)
def atualizar(id, tipo, arquivo, origem, total_registros, status, data_execucao, sucesso, erros, log):
    dto = ImportacaoInputDTO(
        tipo=tipo,
        arquivo=arquivo,
        origem=origem,
        total_registros=total_registros,
        status=status,
        data_execucao=data_execucao,
        sucesso=sucesso,
        erros=erros,
        log=log
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Importação {atualizado.id} atualizada com sucesso")

@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.tipo} - {item.status}")

@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Importação não encontrada")

@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Importação removida com sucesso")
    else:
        click.echo("Falha ao remover")

importacao.add_command(cadastrar)
importacao.add_command(atualizar)
importacao.add_command(consultar)
importacao.add_command(buscar)
importacao.add_command(remover)
