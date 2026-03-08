# ============================================================
# CLI: empreendimento_cli.py
# Camada: interface/cli/
# Descrição: Interface de linha de comando para gerenciamento
#            de empreendimentos. Chama apenas o Service.
# Uso: python -m src.interface.cli.empreendimento_cli [COMANDO]
# Comandos: cadastrar | atualizar | consultar | buscar |
#           listar-disponiveis | listar-incorporadora | remover
# ATENÇÃO API FUTURA: toda lógica está no Service. Para expor
#            via API, basta criar controller que chame os mesmos métodos.
# Sprint: 10.5 — filtros de preco/metragem removidos (agora em unidades)
# ============================================================

import click
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO

repo = EmpreendimentoRepository()
service = EmpreendimentoService(repo)


@click.group()
def empreendimento():
    """Gerenciamento de Empreendimentos imobiliários.

    Empreendimento = contexto institucional do produto.
    Dados comerciais (preço, metragem, tipologia) estão nas unidades.
    Use 'empreendimento COMANDO --help' para detalhes.
    """
    pass


# ----------------------------------------------------------
# CADASTRAR
# ----------------------------------------------------------
@empreendimento.command()
@click.option("--nome",                 required=True,  type=str,   help="Nome comercial do empreendimento")
@click.option("--cidade",               required=False, type=str,   help="Cidade")
@click.option("--estado",               required=False, type=str,   help="Estado (sigla: SP, RJ...)")
@click.option("--bairro",               required=False, type=str,   help="Bairro")
@click.option("--regiao",               required=False, type=str,   help="Região (ex: Zona Sul, Grande ABC)")
@click.option("--endereco",             required=False, type=str,   help="Endereço completo")
@click.option("--produto",              required=False, type=str,   help="Tipo de produto (ex: residencial vertical)")
@click.option("--tipo",                 required=False, type=str,   help="Tipo (apartamento / casa / studio...)")
@click.option("--descricao",            required=False, type=str,   help="Descrição comercial")
@click.option("--lancamento",           required=False, type=str,   help="Período de lançamento (ex: Q1/2025)")
@click.option("--data-entrega",         required=False, type=str,   help="Data de entrega (YYYY-MM-DD)")
@click.option("--status",               required=False, type=str,   help="Status: em obras / pronto / entregue")
@click.option("--total-unidades",       required=False, type=int,   help="Total de unidades do empreendimento")
@click.option("--incorporadora-id",     required=False, type=int,   help="ID da incorporadora")
@click.option("--proprietario-id",      required=False, type=int,   help="ID da construtora proprietária")
@click.option("--spe-id",               required=False, type=int,   help="ID da SPE")
def cadastrar(nome, cidade, estado, bairro, regiao, endereco, produto, tipo,
              descricao, lancamento, data_entrega, status, total_unidades,
              incorporadora_id, proprietario_id, spe_id):
    """Cadastra um novo empreendimento."""
    dto = EmpreendimentoInputDTO(
        nome=nome,
        cidade=cidade,
        estado=estado,
        bairro=bairro,
        regiao=regiao,
        endereco=endereco,
        produto=produto,
        tipo=tipo,
        descricao=descricao,
        periodo_lancamento=lancamento,
        data_entrega=data_entrega,
        status_entrega=status,
        total_unidades=total_unidades,
        amenities=None,
        padrao_construtivo=None,
        incorporadora_id=incorporadora_id,
        proprietario_id=proprietario_id,
        spe_id=spe_id,
        unidade_referencia_id=None
    )
    criado = service.cadastrar(dto)
    click.echo(f"\n✅ Empreendimento cadastrado com sucesso!")
    click.echo(f"   ID      : {criado.id}")
    click.echo(f"   Nome    : {criado.nome}")
    click.echo(f"   Local   : {criado.cidade}/{criado.estado}")
    click.echo(f"   Status  : {criado.status_entrega or '-'}")


# ----------------------------------------------------------
# ATUALIZAR
# ----------------------------------------------------------
@empreendimento.command()
@click.argument("id", type=int)
@click.option("--nome",                 required=False, type=str)
@click.option("--cidade",               required=False, type=str)
@click.option("--estado",               required=False, type=str)
@click.option("--bairro",               required=False, type=str)
@click.option("--regiao",               required=False, type=str)
@click.option("--endereco",             required=False, type=str)
@click.option("--produto",              required=False, type=str)
@click.option("--tipo",                 required=False, type=str)
@click.option("--descricao",            required=False, type=str)
@click.option("--lancamento",           required=False, type=str)
@click.option("--data-entrega",         required=False, type=str)
@click.option("--status",               required=False, type=str)
@click.option("--total-unidades",       required=False, type=int)
@click.option("--incorporadora-id",     required=False, type=int)
@click.option("--proprietario-id",      required=False, type=int)
@click.option("--spe-id",               required=False, type=int)
def atualizar(id, nome, cidade, estado, bairro, regiao, endereco, produto,
              tipo, descricao, lancamento, data_entrega, status,
              total_unidades, incorporadora_id, proprietario_id, spe_id):
    """Atualiza os dados de um empreendimento existente. Requer o ID."""
    dto = EmpreendimentoInputDTO(
        nome=nome,
        cidade=cidade,
        estado=estado,
        bairro=bairro,
        regiao=regiao,
        endereco=endereco,
        produto=produto,
        tipo=tipo,
        descricao=descricao,
        periodo_lancamento=lancamento,
        data_entrega=data_entrega,
        status_entrega=status,
        total_unidades=total_unidades,
        amenities=None,
        padrao_construtivo=None,
        incorporadora_id=incorporadora_id,
        proprietario_id=proprietario_id,
        spe_id=spe_id,
        unidade_referencia_id=None
    )
    atualizado = service.atualizar(id, dto)
    if not atualizado:
        click.echo(f"\n❌ Empreendimento ID {id} não encontrado.")
        return
    click.echo(f"\n✅ Empreendimento {atualizado.id} atualizado com sucesso!")


# ----------------------------------------------------------
# CONSULTAR COM FILTROS
# ----------------------------------------------------------
@empreendimento.command()
@click.option("--cidade",               required=False, type=str,   help="Filtrar por cidade")
@click.option("--regiao",               required=False, type=str,   help="Filtrar por região")
@click.option("--status",               required=False, type=str,   help="Filtrar por status de entrega")
@click.option("--lancamento",           required=False, type=str,   help="Filtrar por período de lançamento")
@click.option("--incorporadora-id",     required=False, type=int,   help="Filtrar por incorporadora")
@click.option("--ordenar-por",          required=False, type=str,   help="Campo: nome / cidade / regiao / entrega")
@click.option("--ordem",                default="asc",  type=str,   show_default=True)
def consultar(cidade, regiao, status, lancamento, incorporadora_id, ordenar_por, ordem):
    """Consulta empreendimentos com filtros.

    Filtros de preço e metragem foram removidos (Sprint 10.5).
    Para filtrar por preço/metragem use: unidade consultar
    """
    results = service.consultar(
        cidade=cidade,
        regiao=regiao,
        status_entrega=status,
        periodo_lancamento=lancamento,
        incorporadora_id=incorporadora_id,
        ordenar_por=ordenar_por,
        ordem=ordem
    )
    if not results:
        click.echo("\nNenhum empreendimento encontrado.")
        return

    click.echo(f"\n{'ID':<6} {'Nome':<30} {'Cidade':<20} {'UF':<4} {'Status':<12} {'Unidades'}")
    click.echo("-" * 80)
    for r in results:
        click.echo(
            f"{r.id:<6} {(r.nome or '-'):<30} {(r.cidade or '-'):<20} "
            f"{(r.estado or '-'):<4} {(r.status_entrega or '-'):<12} "
            f"{r.total_unidades or '-'}"
        )
    click.echo(f"\nTotal: {len(results)} empreendimento(s)")


# ----------------------------------------------------------
# BUSCAR POR ID — ficha completa
# ----------------------------------------------------------
@empreendimento.command()
@click.argument("id", type=int)
def buscar(id):
    """Exibe todos os dados de um empreendimento pelo ID."""
    r = service.buscar_por_id(id)
    if not r:
        click.echo(f"\n❌ Empreendimento ID {id} não encontrado.")
        return

    click.echo(f"\n{'='*45}")
    click.echo(f"  EMPREENDIMENTO #{r.id} — {r.nome or 'sem nome'}")
    click.echo(f"{'='*45}")
    click.echo(f"  Produto          : {r.produto or '-'}")
    click.echo(f"  Tipo             : {r.tipo or '-'}")
    click.echo(f"  Localização      : {r.bairro or '-'}, {r.cidade or '-'} - {r.estado or '-'}")
    click.echo(f"  Região           : {r.regiao or '-'}")
    click.echo(f"  Endereço         : {r.endereco or '-'}")
    click.echo(f"  Lançamento       : {r.periodo_lancamento or '-'}")
    click.echo(f"  Entrega          : {r.data_entrega or '-'}")
    click.echo(f"  Status           : {r.status_entrega or '-'}")
    click.echo(f"  Total unidades   : {r.total_unidades or '-'}")
    click.echo(f"  Incorporadora ID : {r.incorporadora_id or '-'}")
    click.echo(f"  Proprietário ID  : {r.proprietario_id or '-'}")
    click.echo(f"  SPE ID           : {r.spe_id or '-'}")
    click.echo(f"  Unid. referência : {r.unidade_referencia_id or '-'}")
    click.echo(f"  Descrição        : {r.descricao or '-'}")
    click.echo(f"  Amenities        : {r.amenities or '-'}")
    click.echo(f"  Padrão construtivo: {r.padrao_construtivo or '-'}")


# ----------------------------------------------------------
# LISTAR COM UNIDADES DISPONÍVEIS
# ----------------------------------------------------------
@empreendimento.command("listar-disponiveis")
def listar_disponiveis():
    """Lista empreendimentos que ainda têm unidades disponíveis para venda."""
    results = service.listar_com_unidades_disponiveis()
    if not results:
        click.echo("\nNenhum empreendimento com unidades disponíveis.")
        return

    click.echo(f"\n{'ID':<6} {'Nome':<30} {'Cidade':<20} {'Status'}")
    click.echo("-" * 70)
    for r in results:
        click.echo(
            f"{r.id:<6} {(r.nome or '-'):<30} "
            f"{(r.cidade or '-'):<20} {r.status_entrega or '-'}"
        )
    click.echo(f"\nTotal: {len(results)} empreendimento(s) com unidades disponíveis")


# ----------------------------------------------------------
# LISTAR POR INCORPORADORA
# ----------------------------------------------------------
@empreendimento.command("listar-incorporadora")
@click.argument("incorporadora_id", type=int)
def listar_incorporadora(incorporadora_id):
    """Lista todos os empreendimentos de uma incorporadora.

    Exemplo: empreendimento listar-incorporadora 3
    """
    results = service.listar_por_incorporadora(incorporadora_id)
    if not results:
        click.echo(f"\nNenhum empreendimento para a incorporadora {incorporadora_id}.")
        return

    click.echo(f"\nIncorporadora #{incorporadora_id} — {len(results)} empreendimento(s)\n")
    for r in results:
        click.echo(f"  [{r.id}] {r.nome or '-'} — {r.cidade or '-'}/{r.estado or '-'} — {r.status_entrega or '-'}")


# ----------------------------------------------------------
# REMOVER
# ----------------------------------------------------------
@empreendimento.command()
@click.argument("id", type=int)
@click.confirmation_option(prompt="⚠️  Confirma a remoção deste empreendimento?")
def remover(id):
    """Remove um empreendimento pelo ID. Solicita confirmação.

    ATENÇÃO: falhará se houver unidades vinculadas (integridade referencial).
    Remova as unidades primeiro.
    """
    ok = service.remover(id)
    if ok:
        click.echo(f"\n✅ Empreendimento {id} removido com sucesso.")
    else:
        click.echo(f"\n❌ Empreendimento ID {id} não encontrado.")


if __name__ == "__main__":
    empreendimento()