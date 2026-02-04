import click
from src.application.incorporadora_imobiliaria.services.incorporadora_imobiliaria_service import IncorporadoraImobiliariaService
from src.infrastructure.incorporadora_imobiliaria.repositories.incorporadora_imobiliaria_repository import IncorporadoraImobiliariaRepository
from src.domain.incorporadora_imobiliaria.dto.incorporadora_imobiliaria_input_dto import IncorporadoraImobiliariaInputDTO

repo = IncorporadoraImobiliariaRepository()
service = IncorporadoraImobiliariaService(repo)

@click.group()
def incorporadora_imobiliaria():
    """Gerenciamento da relação Incorporadora ↔ Imobiliária"""
    pass

# ---------------------------------------------------------
# Cadastrar
# ---------------------------------------------------------
@click.command()
@click.option("--incorporadora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--observacoes", required=False, type=str, default=None)
def cadastrar(incorporadora_id, imobiliaria_id, observacoes):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=incorporadora_id,
        imobiliaria_id=imobiliaria_id,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"Cadastrado: {criado.incorporadora_id} ↔ {criado.imobiliaria_id}")

# ---------------------------------------------------------
# Atualizar
# ---------------------------------------------------------
@click.command()
@click.option("--incorporadora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
@click.option("--observacoes", required=False, type=str, default=None)
def atualizar(incorporadora_id, imobiliaria_id, observacoes):
    dto = IncorporadoraImobiliariaInputDTO(
        incorporadora_id=incorporadora_id,
        imobiliaria_id=imobiliaria_id,
        observacoes=observacoes
    )
    atualizado = service.atualizar(dto)
    click.echo(f"Atualizado: {atualizado.incorporadora_id} ↔ {atualizado.imobiliaria_id}")

# ---------------------------------------------------------
# Consultar
# ---------------------------------------------------------
@click.command()
def consultar():
    lista = service.consultar()
    for item in lista:
        click.echo(f"{item.incorporadora_id} ↔ {item.imobiliaria_id} | {item.observacoes}")

# ---------------------------------------------------------
# Buscar por IDs
# ---------------------------------------------------------
@click.command()
@click.option("--incorporadora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def buscar(incorporadora_id, imobiliaria_id):
    encontrado = service.buscar_por_ids(incorporadora_id, imobiliaria_id)
    if encontrado:
        click.echo(f"{encontrado.incorporadora_id} ↔ {encontrado.imobiliaria_id} | {encontrado.observacoes}")
    else:
        click.echo("Registro não encontrado")

# ---------------------------------------------------------
# Remover
# ---------------------------------------------------------
@click.command()
@click.option("--incorporadora_id", required=True, type=int)
@click.option("--imobiliaria_id", required=True, type=int)
def remover(incorporadora_id, imobiliaria_id):
    ok = service.remover(incorporadora_id, imobiliaria_id)
    if ok:
        click.echo("Removido com sucesso")
    else:
        click.echo("Nenhum registro removido")

# Registrar comandos no grupo
incorporadora_imobiliaria.add_command(cadastrar)
incorporadora_imobiliaria.add_command(atualizar)
incorporadora_imobiliaria.add_command(consultar)
incorporadora_imobiliaria.add_command(buscar)
incorporadora_imobiliaria.add_command(remover)
