# ============================================================
# DTO: EmpreendimentoNormalizedDTO
# Camada: domain/empreendimento/dto/
# Descrição: Dados já normalizados prontos para persistência.
#            Produzido pelo EmpreendimentoNormalizer a partir de
#            dados brutos (planilha, CLI, futura API).
#            Não tem id — ainda não foi persistido.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class EmpreendimentoNormalizedDTO:
    # Identificação principal
    nome: Optional[str] = None              # normalizado: strip

    # Localização
    regiao: Optional[str] = None            # normalizado: strip
    bairro: Optional[str] = None            # normalizado: strip
    cidade: Optional[str] = None            # normalizado: strip + title case
    estado: Optional[str] = None            # normalizado: upper + strip (ex: "sp" → "SP")
    endereco: Optional[str] = None          # normalizado: strip

    # Caracterização do produto
    produto: Optional[str] = None           # normalizado: strip
    tipo: Optional[str] = None              # normalizado: lower + strip
    descricao: Optional[str] = None         # normalizado: strip

    # Cronograma
    periodo_lancamento: Optional[str] = None # normalizado: strip
    data_entrega: Optional[str] = None      # normalizado: formato ISO YYYY-MM-DD
    status_entrega: Optional[str] = None    # normalizado: lower + strip
                                            # valores aceitos: em obras / pronto / entregue

    # Atributos institucionais
    total_unidades: Optional[int] = None    # normalizado: int, None se inválido
    amenities: Optional[str] = None         # normalizado: JSON string válido ou None
    padrao_construtivo: Optional[str] = None # normalizado: JSON string válido ou None

    # Relacionamentos — validados como int
    incorporadora_id: Optional[int] = None
    proprietario_id: Optional[int] = None
    spe_id: Optional[int] = None
    unidade_referencia_id: Optional[int] = None

    # CAMPOS REMOVIDOS NA SPRINT 10.5 — NÃO REINTRODUZIR:
    # preco, tipologia, metragem_min, metragem_max → agora em unidades