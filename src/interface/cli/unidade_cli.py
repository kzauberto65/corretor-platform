# ============================================================
# CLI: unidade_cli.py
# Camada: interface/cli/
# Descrição: Interface de linha de comando para gerenciamento
#            de unidades. Chama apenas o Service — nunca o
#            Repository ou Engine diretamente.
# Uso: python -m src.interface.cli.unidade_cli [COMANDO] [OPÇÕES]
# Comandos: cadastrar | atualizar | disponibilidade | consultar |
#           buscar | listar-por-empreendimento | remover
# ATENÇÃO API FUTURA: toda lógica está no Service. Para expor via
#            API, basta criar um controller que chame os mesmos métodos.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

import click
from src.application.unidade.services.unidade_service import UnidadeService
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository
from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO

# Instanciação do service com repository padrão
# Em produção futura: injetar via container de dependências
repo = UnidadeRepository()
service = UnidadeService(repo)


@click.group()
def unidade():
    """Gerenciamento de Unidades imobiliárias.

    Cada unidade é um imóvel comercializável vinculado a um empreendimento.
    Use 'unidade COMANDO --help' para detalhes de cada comando.
    """
    pass


# ----------------------------------------------------------
# CADASTRAR
# ----------------------------------------------------------
@unidade.command()
@click.option("--empreendimento-id",    required=True,  type=int,   help="ID do empreendimento ao qual a unidade pertence")
@click.option("--codigo",               required=False, type=str,   help="Código da unidade (ex: AP-101, GARDEN-02)")
@click.option("--preco",                required=False, type=float, help="Preço de venda em R$")
@click.option("--metragem",             required=False, type=float, help="Área privativa em m²")
@click.option("--dormitorios",          required=False, type=int,   help="Número de dormitórios")
@click.option("--suites",               required=False, type=int,   help="Número de suítes")
@click.option("--vagas",                required=False, type=int,   help="Vagas de garagem")
@click.option("--tipo",                 required=False, type=str,   help="Tipologia: studio / 1dorm / 2dorm / garden / cobertura / casa")
@click.option("--andar",                required=False, type=int,   help="Andar (0 = térreo)")
@click.option("--disponibilidade",      required=False, type=str,   default="disponível", show_default=True, help="Status: disponível / vendido / reservado")
@click.option("--descricao",            required=False, type=str,   help="Descrição comercial da unidade")
@click.option("--observacoes",          required=False, type=str,   help="Notas internas")
def cadastrar(empreendimento_id, codigo, preco, metragem, dormitorios,
              suites, vagas, tipo, andar, disponibilidade, descricao, observacoes):
    """Cadastra uma nova unidade em um empreendimento."""
    dto = UnidadeInputDTO(
        empreendimento_id=empreendimento_id,
        codigo_unidade=codigo,
        preco=preco,
        metragem=metragem,
        dormitorios=dormitorios,
        suites=suites,
        vagas=vagas,
        tipo_unidade=tipo,
        andar=andar,
        disponibilidade=disponibilidade,
        descricao_unidade=descricao,
        observacoes=observacoes
    )
    criado = service.cadastrar(dto)
    click.echo(f"\n✅ Unidade cadastrada com sucesso!")
    click.echo(f"   ID          : {criado.id}")
    click.echo(f"   Código      : {criado.codigo_unidade or '-'}")
    click.echo(f"   Tipo        : {criado.tipo_unidade or '-'}")
    click.echo(f"   Preço       : R$ {criado.preco:,.0f}".replace(",", ".") if criado.preco else "   Preço       : -")
    click.echo(f"   Metragem    : {criado.metragem}m²" if criado.metragem else "   Metragem    : -")
    click.echo(f"   Disponível  : {criado.disponibilidade}")


# ----------------------------------------------------------
# ATUALIZAR
# ----------------------------------------------------------
@unidade.command()
@click.argument("id", type=int)
@click.option("--empreendimento-id",    required=True,  type=int,   help="ID do empreendimento")
@click.option("--codigo",               required=False, type=str,   help="Código da unidade")
@click.option("--preco",                required=False, type=float, help="Preço de venda em R$")
@click.option("--metragem",             required=False, type=float, help="Área privativa em m²")
@click.option("--dormitorios",          required=False, type=int,   help="Número de dormitórios")
@click.option("--suites",               required=False, type=int,   help="Número de suítes")
@click.option("--vagas",                required=False, type=int,   help="Vagas de garagem")
@click.option("--tipo",                 required=False, type=str,   help="Tipologia da unidade")
@click.option("--andar",                required=False, type=int,   help="Andar")
@click.option("--disponibilidade",      required=False, type=str,   help="Status de disponibilidade")
@click.option("--descricao",            required=False, type=str,   help="Descrição comercial")
@click.option("--observacoes",          required=False, type=str,   help="Notas internas")
def atualizar(id, empreendimento_id, codigo, preco, metragem, dormitorios,
              suites, vagas, tipo, andar, disponibilidade, descricao, observacoes):
    """Atualiza os dados de uma unidade existente. Requer o ID da unidade."""
    dto = UnidadeInputDTO(
        empreendimento_id=empreendimento_id,
        codigo_unidade=codigo,
        preco=preco,
        metragem=metragem,
        dormitorios=dormitorios,
        suites=suites,
        vagas=vagas,
        tipo_unidade=tipo,
        andar=andar,
        disponibilidade=disponibilidade,
        descricao_unidade=descricao,
        observacoes=observacoes
    )
    atualizado = service.atualizar(id, dto)
    if not atualizado:
        click.echo(f"\n❌ Unidade ID {id} não encontrada.")
        return
    click.echo(f"\n✅ Unidade {atualizado.id} atualizada com sucesso!")


# ----------------------------------------------------------
# DISPONIBILIDADE — atualização rápida de status
# ----------------------------------------------------------
@unidade.command()
@click.argument("id", type=int)
@click.argument("status", type=click.Choice(["disponível", "vendido", "reservado"]))
def disponibilidade(id, status):
    """Atualiza o status de disponibilidade de uma unidade.

    STATUS: disponível | vendido | reservado

    Exemplo: unidade disponibilidade 42 vendido
    """
    ok = service.atualizar_disponibilidade(id, status)
    if ok:
        click.echo(f"\n✅ Unidade {id} marcada como '{status}'.")
    else:
        click.echo(f"\n❌ Falha ao atualizar unidade {id}.")


# ----------------------------------------------------------
# CONSULTAR — listagem geral
# ----------------------------------------------------------
@unidade.command()
def consultar():
    """Lista todas as unidades cadastradas (incluindo vendidas e reservadas)."""
    lista = service.consultar()
    if not lista:
        click.echo("\nNenhuma unidade cadastrada.")
        return

    click.echo(f"\n{'ID':<6} {'Empr.':<7} {'Código':<12} {'Tipo':<12} {'Dorms':<6} {'Vagas':<6} {'Preço':>14} {'Situação'}")
    click.echo("-" * 75)
    for u in lista:
        preco_fmt = f"R$ {u.preco:,.0f}".replace(",", ".") if u.preco else "-"
        click.echo(
            f"{u.id:<6} {u.empreendimento_id:<7} {u.codigo_unidade or '-':<12} "
            f"{u.tipo_unidade or '-':<12} {u.dormitorios or '-':<6} {u.vagas or '-':<6} "
            f"{preco_fmt:>14} {u.disponibilidade or '-'}"
        )
    click.echo(f"\nTotal: {len(lista)} unidade(s)")


# ----------------------------------------------------------
# BUSCAR — detalhe de uma unidade
# ----------------------------------------------------------
@unidade.command()
@click.argument("id", type=int)
def buscar(id):
    """Exibe os detalhes completos de uma unidade pelo ID."""
    u = service.buscar_por_id(id)
    if not u:
        click.echo(f"\n❌ Unidade ID {id} não encontrada.")
        return

    click.echo(f"\n{'='*40}")
    click.echo(f"  UNIDADE #{u.id} — {u.codigo_unidade or 'sem código'}")
    click.echo(f"{'='*40}")
    click.echo(f"  Empreendimento : {u.empreendimento_id}")
    click.echo(f"  Tipo           : {u.tipo_unidade or '-'}")
    click.echo(f"  Andar          : {u.andar if u.andar is not None else '-'}")
    click.echo(f"  Preço          : R$ {u.preco:,.0f}".replace(",", ".") if u.preco else "  Preço          : -")
    click.echo(f"  Metragem       : {u.metragem}m²" if u.metragem else "  Metragem       : -")
    click.echo(f"  Dormitórios    : {u.dormitorios or '-'}")
    click.echo(f"  Suítes         : {u.suites or '-'}")
    click.echo(f"  Vagas          : {u.vagas or '-'}")
    click.echo(f"  Disponibilidade: {u.disponibilidade or '-'}")
    click.echo(f"  Descrição      : {u.descricao_unidade or '-'}")
    click.echo(f"  Observações    : {u.observacoes or '-'}")
    click.echo(f"  Criado em      : {u.created_at or '-'}")


# ----------------------------------------------------------
# LISTAR POR EMPREENDIMENTO
# ----------------------------------------------------------
@unidade.command("listar-empreendimento")
@click.argument("empreendimento_id", type=int)
def listar_empreendimento(empreendimento_id):
    """Lista todas as unidades de um empreendimento (inclusive vendidas).

    Exemplo: unidade listar-empreendimento 5
    """
    lista = service.listar_por_empreendimento(empreendimento_id)
    if not lista:
        click.echo(f"\nNenhuma unidade encontrada para o empreendimento {empreendimento_id}.")
        return

    # Resumo de disponibilidade
    resumo = service.resumo_empreendimento(empreendimento_id)
    click.echo(f"\nEmpreendimento #{empreendimento_id} — {len(lista)} unidade(s)")
    click.echo(f"  Disponíveis: {resumo.get('disponível', 0)} | "
               f"Vendidas: {resumo.get('vendido', 0)} | "
               f"Reservadas: {resumo.get('reservado', 0)}")
    click.echo("-" * 70)

    click.echo(f"\n{'ID':<6} {'Código':<12} {'Tipo':<12} {'Dorms':<6} {'Vagas':<6} {'Preço':>14} {'Situação'}")
    click.echo("-" * 70)
    for u in lista:
        preco_fmt = f"R$ {u.preco:,.0f}".replace(",", ".") if u.preco else "-"
        click.echo(
            f"{u.id:<6} {u.codigo_unidade or '-':<12} {u.tipo_unidade or '-':<12} "
            f"{u.dormitorios or '-':<6} {u.vagas or '-':<6} "
            f"{preco_fmt:>14} {u.disponibilidade or '-'}"
        )


# ----------------------------------------------------------
# REMOVER
# ----------------------------------------------------------
@unidade.command()
@click.argument("id", type=int)
@click.confirmation_option(prompt="⚠️  Confirma a remoção desta unidade?")
def remover(id):
    """Remove uma unidade pelo ID. Solicita confirmação antes de executar."""
    ok = service.remover(id)
    if ok:
        click.echo(f"\n✅ Unidade {id} removida com sucesso.")
    else:
        click.echo(f"\n❌ Unidade ID {id} não encontrada.")


if __name__ == "__main__":
    unidade()