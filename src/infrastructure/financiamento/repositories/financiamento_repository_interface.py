"""
Interface do Repositório de Financiamento.
Define o contrato que a camada de Infraestrutura deverá implementar.
"""
from abc import ABC, abstractmethod
from typing import Optional
from src.domain.financiamento.entities.tabela_financiamento import TabelaFinanciamento

class IFinanciamentoRepository(ABC):
    
    @abstractmethod
    def cadastrar(self, financiamento: TabelaFinanciamento) -> TabelaFinanciamento:
        """Persiste uma nova tabela de financiamento e retorna a entidade com ID criado."""
        pass

    @abstractmethod
    def buscar_por_unidade(self, unidade_id: int) -> Optional[TabelaFinanciamento]:
        """Retorna o financiamento satélite associado a uma unidade (0 ou 1)."""
        pass