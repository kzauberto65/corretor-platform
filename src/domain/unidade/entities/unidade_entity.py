# ============================================================
# ENTITY: UnidadeEntity
# Camada: domain/unidade/entities/
# Sprint: 10.5 — alinhado ao novo schema e ADR-001
# ============================================================

from dataclasses import dataclass, asdict

# Import da entidade de Financiamento (Tabela Satélite do ADR-005)
from src.domain.financiamento.entities.tabela_financiamento import TabelaFinanciamento


@dataclass
class UnidadeEntity:
    # Identidade no banco — nunca None após persistido
    id: int | None = None

    # Vínculo obrigatório com o empreendimento (contexto institucional)
    empreendimento_id: int | None = None

    # Identificação da unidade
    codigo_unidade: str | None = None       # ex: AP-101, GARDEN-02, COB-PH

    # Atributos comerciais — base para vetorização no IAEngine
    preco: float | None = None              # preço de venda em R$
    metragem: float | None = None           # área privativa em m²
    dormitorios: int | None = None          # número de dormitórios
    suites: int | None = None               # número de suítes
    vagas: int | None = None                # vagas de garagem

    # Tipologia e posição
    tipo_unidade: str | None = None         # studio / 1dorm / 2dorm / garden / cobertura / casa
    andar: int | None = None                # andar (0 = térreo)

    # Status comercial — usado pelo Matching para filtrar disponíveis
    disponibilidade: str | None = None      # disponível / vendido / reservado

    # Descrição e notas
    descricao_unidade: str | None = None    # descrição comercial (exibida ao cliente)
    observacoes: str | None = None          # notas internas (não exibidas ao cliente)

    # Auditoria
    created_at: str | None = None           # datetime ISO gerado automaticamente pelo banco

    # ============================================================
    # ADR-005: Relacionamento 1:1 com Financiamento Satélite
    # ============================================================
    financiamento_satelite: TabelaFinanciamento | None = None

    def vincular_financiamento(self, financiamento: TabelaFinanciamento) -> None:
        """
        Associa um financiamento satélite a esta unidade (relacionamento 1:1).
        Garante que o financiamento pertence a esta unidade mapeada.
        """
        if self.id is None:
            raise ValueError("A unidade precisa ter um ID (ser persistida) antes de vincular um financiamento.")
        if financiamento.unidade_id != self.id:
            raise ValueError("Este financiamento pertence a outra unidade (unidade_id não confere).")
            
        self.financiamento_satelite = financiamento

    def is_disponivel(self) -> bool:
        """Verifica se a unidade está disponível para venda.
        Usado pelo Matching e IA para filtrar antes de processar."""
        return self.disponibilidade == "disponível"

    def resumo_comercial(self) -> str:
        """Retorna uma linha de descrição comercial da unidade.
        Útil para exibição em CLI, WhatsApp e futuras UIs."""
        tipo = self.tipo_unidade or "unidade"
        dorms = f"{self.dormitorios} dorm" if self.dormitorios else ""
        metros = f"{self.metragem}m²" if self.metragem else ""
        preco = f"R$ {self.preco:,.0f}".replace(",", ".") if self.preco else ""
        partes = [p for p in [tipo, dorms, metros, preco] if p]
        return " | ".join(partes) or self.codigo_unidade or "Unidade sem descrição"

    def to_dict(self) -> dict:
        """Serializa a entity para dict."""
        return asdict(self)