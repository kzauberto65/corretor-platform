"""
Entidade de Domínio: Tabela de Financiamento.
Contém as regras de negócio e validações de elegibilidade da unidade.
"""
from dataclasses import dataclass
from typing import Optional
from src.domain.financiamento.enums.perfil_comprador_enum import PerfilCompradorEnum
from src.domain.financiamento.enums.condicao_uso_enum import CondicaoUsoEnum

@dataclass
class TabelaFinanciamento:
    unidade_id: int
    perfil_comprador: PerfilCompradorEnum
    condicao_uso: CondicaoUsoEnum
    valor_entrada: float
    valor_mensais: float
    qtde_mensais: int
    valor_intermediarias: float
    qtde_intermediarias: int
    valor_chaves: float
    valor_financiamento: float
    renda_minima_exigida: Optional[float] = None
    renda_teto_familiar: Optional[float] = None
    id: Optional[int] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        """
        Executado automaticamente após a inicialização da classe.
        Aplica regras de negócio rígidas do domínio imobiliário.
        """
        self.validar_regras_sociais()

    def validar_regras_sociais(self):
        """
        Garante que unidades HIS e HMP não sejam marcadas para investidores
        ou para rentabilidade de curta duração.
        """
        perfis_sociais = [PerfilCompradorEnum.HIS, PerfilCompradorEnum.HMP]
        
        if self.perfil_comprador in perfis_sociais:
            if self.condicao_uso != CondicaoUsoEnum.MORADIA_PROPRIA:
                raise ValueError(
                    f"Regra de Domínio Violada: O perfil {self.perfil_comprador.value} "
                    f"permite apenas a condição de uso '{CondicaoUsoEnum.MORADIA_PROPRIA.value}'."
                )
        
        # Correção: Blinda a checagem verificando se o valor é diferente de None antes da matemática
        if self.renda_minima_exigida is not None and self.renda_minima_exigida < 0:
            raise ValueError("A renda mínima exigida não pode ser negativa.")