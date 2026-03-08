"""
Serviço de Aplicação para Tabela de Financiamento.
Orquestra o mapeamento de DTOs, entidades e chamadas de repositório.
"""
from typing import List, Optional
from src.domain.financiamento.enums.perfil_comprador_enum import PerfilCompradorEnum
from src.domain.financiamento.enums.condicao_uso_enum import CondicaoUsoEnum
from src.domain.financiamento.entities.tabela_financiamento import TabelaFinanciamento
from src.domain.financiamento.dto.tabela_financiamento_dto import TabelaFinanciamentoInputDTO, TabelaFinanciamentoOutputDTO
from src.infrastructure.financiamento.repositories.financiamento_repository_interface import IFinanciamentoRepository

class FinanciamentoService:
    def __init__(self, repository: IFinanciamentoRepository):
        self._repository = repository

    def cadastrar(self, dto: TabelaFinanciamentoInputDTO) -> TabelaFinanciamentoOutputDTO:
        """
        Coordena a criação de um financiamento.
        Valida entradas, instancia a entidade e salva no repositório.
        """
        # Converter strings para Enums de domínio (caso venham assim)
        try:
            perfil_enum = PerfilCompradorEnum(dto.perfil_comprador)
            condicao_enum = CondicaoUsoEnum(dto.condicao_uso)
        except ValueError as e:
            raise ValueError(f"Valor de Enum inválido: {e}")

        entidade = TabelaFinanciamento(
            unidade_id=dto.unidade_id,
            perfil_comprador=perfil_enum,
            condicao_uso=condicao_enum,
            valor_entrada=dto.valor_entrada,
            valor_mensais=dto.valor_mensais,
            qtde_mensais=dto.qtde_mensais,
            valor_intermediarias=dto.valor_intermediarias,
            qtde_intermediarias=dto.qtde_intermediarias,
            valor_chaves=dto.valor_chaves,
            valor_financiamento=dto.valor_financiamento,
            renda_minima_exigida=dto.renda_minima_exigida,
            renda_teto_familiar=dto.renda_teto_familiar
        )

        entidade_salva = self._repository.cadastrar(entidade)

        return TabelaFinanciamentoOutputDTO(
            id=entidade_salva.id,
            unidade_id=entidade_salva.unidade_id,
            perfil_comprador=entidade_salva.perfil_comprador.value,
            condicao_uso=entidade_salva.condicao_uso.value,
            valor_entrada=entidade_salva.valor_entrada,
            valor_mensais=entidade_salva.valor_mensais,
            qtde_mensais=entidade_salva.qtde_mensais,
            valor_intermediarias=entidade_salva.valor_intermediarias,
            qtde_intermediarias=entidade_salva.qtde_intermediarias,
            valor_chaves=entidade_salva.valor_chaves,
            valor_financiamento=entidade_salva.valor_financiamento,
            renda_minima_exigida=entidade_salva.renda_minima_exigida,
            renda_teto_familiar=entidade_salva.renda_teto_familiar,
            created_at=entidade_salva.created_at
        )

    def buscar_por_unidade(self, unidade_id: int) -> Optional[TabelaFinanciamentoOutputDTO]:
        """
        Verifica a existência de financiamento vinculado a uma unidade (1:1).
        """
        entidade = self._repository.buscar_por_unidade(unidade_id)
        
        if not entidade:
            return None
            
        return TabelaFinanciamentoOutputDTO(
            id=entidade.id,
            unidade_id=entidade.unidade_id,
            perfil_comprador=entidade.perfil_comprador.value,
            condicao_uso=entidade.condicao_uso.value,
            valor_entrada=entidade.valor_entrada,
            valor_mensais=entidade.valor_mensais,
            qtde_mensais=entidade.qtde_mensais,
            valor_intermediarias=entidade.valor_intermediarias,
            qtde_intermediarias=entidade.qtde_intermediarias,
            valor_chaves=entidade.valor_chaves,
            valor_financiamento=entidade.valor_financiamento,
            renda_minima_exigida=entidade.renda_minima_exigida,
            renda_teto_familiar=entidade.renda_teto_familiar,
            created_at=entidade.created_at
        )