# ============================================================
# ENTITY: EmpreendimentoEntity
# Camada: domain/empreendimento/entities/
# Descrição: Representa um empreendimento já persistido no banco.
#            É o objeto de domínio completo — tem identidade (id).
#            Empreendimento = contexto institucional (Sprint 10.5).
#            NÃO contém dados comerciais — esses vivem em unidades.
#            Usado pelo Repository para mapear rows do SQLite.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class EmpreendimentoEntity:
    # Identidade no banco — nunca None após persistido
    id: Optional[int]

    # Identificação principal
    nome: Optional[str]                     # nome comercial do empreendimento

    # Localização
    regiao: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]                   # sigla: SP, RJ, MG...
    endereco: Optional[str]

    # Caracterização do produto
    produto: Optional[str]                  # ex: residencial vertical, comercial
    tipo: Optional[str]                     # ex: apartamento, casa, studio
    descricao: Optional[str]

    # Cronograma
    periodo_lancamento: Optional[str]
    data_entrega: Optional[str]             # formato ISO: YYYY-MM-DD
    status_entrega: Optional[str]           # em obras / pronto / entregue

    # Atributos institucionais
    total_unidades: Optional[int]           # total de unidades do empreendimento
    amenities: Optional[str]                # JSON com lista de amenidades
    padrao_construtivo: Optional[str]       # JSON com padrão construtivo

    # Relacionamentos institucionais
    incorporadora_id: Optional[int]         # FK → incorporadora(id)
    proprietario_id: Optional[int]          # FK → construtoras(id)
    spe_id: Optional[int]                   # FK → spe(id)
    unidade_referencia_id: Optional[int]    # FK → unidades(id)

    # ----------------------------------------------------------
    # MÉTODOS DE DOMÍNIO
    # ----------------------------------------------------------

    def esta_entregue(self) -> bool:
        """Verifica se o empreendimento já foi entregue.
        Usado pelo IAEngine para calcular urgência × disponibilidade."""
        return self.status_entrega == "entregue"

    def esta_em_obras(self) -> bool:
        """Verifica se o empreendimento está em obras (planta).
        Compradores de planta toleram preço mais alto — dado relevante para IA."""
        return self.status_entrega == "em obras"

    def localizacao_completa(self) -> str:
        """Retorna string de localização formatada para exibição e matching.
        Ex: 'Vila Madalena, São Paulo - SP'"""
        partes = [p for p in [self.bairro, self.cidade, self.estado] if p]
        return ", ".join(partes) if partes else "Localização não informada"

    def resumo(self) -> str:
        """Retorna linha de resumo do empreendimento para CLI e futuras UIs.
        Ex: 'Parque das Flores | Apartamento | Vila Madalena, São Paulo - SP'"""
        partes = [p for p in [self.nome, self.tipo, self.localizacao_completa()] if p]
        return " | ".join(partes) if partes else f"Empreendimento #{self.id}"

    def to_dict(self) -> dict:
        """Serializa a entity para dict.
        Usa dataclasses.asdict — mais seguro que __dict__ para objetos aninhados."""
        return asdict(self)

    # CAMPOS REMOVIDOS NA SPRINT 10.5 — NÃO REINTRODUZIR:
    # preco, tipologia, metragem_min, metragem_max → agora em unidades