# ============================================================
# DTO: UnidadeNormalizedDTO
# Camada: domain/unidade/dto/
# Descrição: Dados já normalizados prontos para persistência.
#            Produzido pelo UnidadeNormalizer a partir de dados
#            brutos (planilha, API, CLI).
#            Estrutura idêntica ao InputDTO — separado por clareza
#            semântica: Input = dado bruto, Normalized = dado limpo.
# Sprint: 10.5 — alinhado ao novo schema
# ============================================================

from dataclasses import dataclass
from typing import Optional


@dataclass
class UnidadeNormalizedDTO:
    # Vínculo obrigatório com o empreendimento
    empreendimento_id: int

    # Identificação da unidade
    codigo_unidade: Optional[str]       # normalizado: strip + upper

    # Atributos comerciais principais
    preco: Optional[float]              # normalizado: float, None se inválido
    metragem: Optional[float]           # normalizado: float, None se inválido
    dormitorios: Optional[int]          # normalizado: int, None se inválido
    suites: Optional[int]               # normalizado: int, 0 se não informado
    vagas: Optional[int]                # normalizado: int, 0 se não informado

    # Tipologia e localização interna
    tipo_unidade: Optional[str]         # normalizado: lower + strip
                                        # valores aceitos: studio / 1dorm / 2dorm /
                                        #                  3dorm / garden / cobertura / casa
    andar: Optional[int]                # normalizado: int, 0 = térreo

    # Status comercial
    disponibilidade: Optional[str]      # normalizado: lower + strip
                                        # valores aceitos: disponível / vendido / reservado

    # Descrição e notas
    descricao_unidade: Optional[str]    # normalizado: strip
    observacoes: Optional[str]          # normalizado: strip