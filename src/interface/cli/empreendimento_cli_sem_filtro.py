import click
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository

repo = EmpreendimentoRepository()
service = EmpreendimentoService(repo)

@click.group()
def empreendimento():
    pass

@empreendimento.command()
@click.option("--regiao")
@click.option("--bairro")
@click.option("--cidade")
@click.option("--estado")
@click.option("--produto")
@click.option("--endereco")
@click.option("--data_entrega")
@click.option("--status_entrega")
@click.option("--tipo")
@click.option("--descricao")
@click.option("--preco", type=float)
@click.option("--proprietario_id", type=int)
@click.option("--incorporadora_id", type=int)
@click.option("--unidade_referencia_id", type=int)
@click.option("--spe_id", type=int)
@click.option("--periodo_lancamento")
@click.option("--nome")
@click.option("--tipologia")
def cadastrar(**kwargs):
    dto = EmpreendimentoInputDTO(**kwargs)
    result = service.cadastrar(dto)
    click.echo(f"Empreendimento cadastrado com ID {result.id}")

@empreendimento.command()
@click.argument("id", type=int)
@click.option("--regiao")
@click.option("--bairro")
@click.option("--cidade")
@click.option("--estado")
@click.option("--produto")
@click.option("--endereco")
@click.option("--data_entrega")
@click.option("--status_entrega")
@click.option("--tipo")
@click.option("--descricao")
@click.option("--preco", type=float)
@click.option("--proprietario_id", type=int)
@click.option("--incorporadora_id", type=int)
@click.option("--unidade_referencia_id", type=int)
@click.option("--spe_id", type=int)
@click.option("--periodo_lancamento")
@click.option("--nome")
@click.option("--tipologia")
def atualizar(id, **kwargs):
    dto = EmpreendimentoInputDTO(**kwargs)
    result = service.atualizar(id, dto)
    if result:
        click.echo(f"Empreendimento {id} atualizado.")
    else:
        click.echo("Empreendimento não encontrado.")

@empreendimento.command()
def consultar():
    results = service.consultar()
    for r in results:
        click.echo(f"{r.id} - {r.nome} - {r.cidade} - {r.estado}")

@empreendimento.command()
@click.argument("id", type=int)
def buscar(id):
    result = service.buscar_por_id(id)
    if result:
        click.echo(result)
    else:
        click.echo("Empreendimento não encontrado.")

@empreendimento.command()
@click.argument("id", type=int)
def remover(id):
    service.remover(id)
    click.echo(f"Empreendimento {id} removido.")

if __name__ == "__main__":
    empreendimento()
