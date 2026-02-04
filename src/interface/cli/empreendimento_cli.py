import click
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService

repo = EmpreendimentoRepository()
service = EmpreendimentoService(repo)

@click.group()
def empreendimento():
    """CLI de Empreendimentos"""
    pass

# ---------------------------------------------------------
# CONSULTAR COM FILTROS
# ---------------------------------------------------------
@empreendimento.command()
@click.option("--cidade")
@click.option("--regiao")
@click.option("--tipologia")
@click.option("--lancamento")
@click.option("--status")
@click.option("--preco-min", type=float)
@click.option("--preco-max", type=float)
@click.option("--ordenar-por")
@click.option("--ordem", default="asc")
def consultar(
    cidade,
    regiao,
    tipologia,
    lancamento,
    status,
    preco_min,
    preco_max,
    ordenar_por,
    ordem
):
    """Consulta empreendimentos com filtros"""
    
    results = service.consultar(
        cidade=cidade,
        regiao=regiao,
        tipologia=tipologia,
        lancamento=lancamento,
        status=status,
        preco_min=preco_min,
        preco_max=preco_max,
        ordenar_por=ordenar_por,
        ordem=ordem
    )

    if not results:
        click.echo("Nenhum empreendimento encontrado.")
        return

    for r in results:
        click.echo(f"{r.id} - {r.nome} - {r.cidade} - {r.estado}")

# ---------------------------------------------------------
# BUSCAR POR ID
# ---------------------------------------------------------
@empreendimento.command()
@click.argument("id", type=int)
def buscar(id):
    """Busca um empreendimento pelo ID"""
    r = service.buscar_por_id(id)
    if not r:
        click.echo("Empreendimento não encontrado.")
    else:
        click.echo(r)

# ---------------------------------------------------------
# REMOVER
# ---------------------------------------------------------
@empreendimento.command()
@click.argument("id", type=int)
def remover(id):
    """Remove um empreendimento"""
    ok = service.remover(id)
    if ok:
        click.echo("Empreendimento removido com sucesso.")
    else:
        click.echo("Erro ao remover empreendimento.")

if __name__ == "__main__":
    empreendimento()
