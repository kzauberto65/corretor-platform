# src/interface/cli/mailing_cli.py

import click

from src.application.mailing.services.mailing_service import MailingService
from src.infrastructure.mailing.repositories.mailing_repository import MailingRepository
from src.domain.mailing.dto.mailing_input_dto import MailingInputDTO

from src.infrastructure.mailing.exporters.mailing_exporter import MailingExporterCompleto
from src.infrastructure.mailing.exporters.mailing_resumido_exporter import MailingExporterResumido


repo = MailingRepository()
service = MailingService(repo)


@click.group()
def mailing():
    """Gerenciamento de mailing"""
    pass


# ---------------------------------------------------------
# CADASTRAR
# ---------------------------------------------------------
@click.command()
@click.option("--nome", required=False)
@click.option("--email", required=False)
@click.option("--telefone", required=False)
@click.option("--origem", required=False)
@click.option("--tags", required=False)
def cadastrar(nome, email, telefone, origem, tags):
    dto = MailingInputDTO(
        nome=nome,
        email=email,
        telefone=telefone,
        origem=origem,
        tags=tags
    )
    criado = service.cadastrar(dto)
    click.echo(f"Mailing cadastrado com ID {criado.id}")


# ---------------------------------------------------------
# ATUALIZAR
# ---------------------------------------------------------
@click.command()
@click.argument("id", type=int)
@click.option("--nome", required=False)
@click.option("--email", required=False)
@click.option("--telefone", required=False)
@click.option("--origem", required=False)
@click.option("--tags", required=False)
def atualizar(id, nome, email, telefone, origem, tags):
    dto = MailingInputDTO(
        nome=nome,
        email=email,
        telefone=telefone,
        origem=origem,
        tags=tags
    )
    atualizado = service.atualizar(id, dto)
    click.echo(f"Mailing {atualizado.id} atualizado com sucesso")


# ---------------------------------------------------------
# CONSULTAR
# ---------------------------------------------------------
@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.id} - {item.nome} - {item.email} - {item.telefone}")


# ---------------------------------------------------------
# BUSCAR POR ID
# ---------------------------------------------------------
@click.command()
@click.argument("id", type=int)
def buscar(id):
    encontrado = service.buscar_por_id(id)
    if encontrado:
        click.echo(encontrado)
    else:
        click.echo("Registro de mailing não encontrado")


# ---------------------------------------------------------
# REMOVER
# ---------------------------------------------------------
@click.command()
@click.argument("id", type=int)
def remover(id):
    ok = service.remover(id)
    if ok:
        click.echo("Registro removido com sucesso")
    else:
        click.echo("Falha ao remover")


# ---------------------------------------------------------
# EXPORTAR COMPLETO
# ---------------------------------------------------------
@click.command()
@click.option("--saida", default="data/exportado", help="Diretório de saída")
def exportar_completo(saida):
    exporter = MailingExporterCompleto(service)
    caminho = exporter.exportar(f"{saida}/mailing_completo.xlsx")
    click.echo(f"Arquivo gerado: {caminho}")


# ---------------------------------------------------------
# EXPORTAR RESUMIDO
# ---------------------------------------------------------
@click.command()
@click.option("--saida", default="data/exportado", help="Diretório de saída")
def exportar_resumido(saida):
    exporter = MailingExporterResumido(service)
    caminho = exporter.exportar(f"{saida}/mailing_resumido.xlsx")
    click.echo(f"Arquivo gerado: {caminho}")


# ---------------------------------------------------------
# REGISTRA OS COMANDOS NO GRUPO
# ---------------------------------------------------------
mailing.add_command(cadastrar)
mailing.add_command(atualizar)
mailing.add_command(consultar)
mailing.add_command(buscar)
mailing.add_command(remover)
mailing.add_command(exportar_completo)
mailing.add_command(exportar_resumido)
