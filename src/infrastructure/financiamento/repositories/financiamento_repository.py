"""
Implementação em SQLite do Repositório de Financiamento.
Implementa a interface definida na camada de domínio.
"""
import sqlite3
from typing import Optional
from src.domain.financiamento.entities.tabela_financiamento import TabelaFinanciamento
from src.infrastructure.financiamento.repositories.financiamento_repository_interface import IFinanciamentoRepository
from src.domain.financiamento.enums.perfil_comprador_enum import PerfilCompradorEnum
from src.domain.financiamento.enums.condicao_uso_enum import CondicaoUsoEnum

class FinanciamentoRepositorySQLite(IFinanciamentoRepository):
    def __init__(self, db_path: str):
        self._db = sqlite3.connect(db_path)

    def cadastrar(self, financiamento: TabelaFinanciamento) -> TabelaFinanciamento:
        """
        Insere a Entidade no banco de dados SQLite e retorna atualizada com ID.
        """
        query = """
            INSERT INTO tabelas_financiamento (
                unidade_id, perfil_comprador, condicao_uso, renda_teto_familiar,
                renda_minima_exigida, valor_entrada, valor_mensais, qtde_mensais,
                valor_intermediarias, qtde_intermediarias, valor_chaves, valor_financiamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        valores = (
            financiamento.unidade_id,
            financiamento.perfil_comprador.value,
            financiamento.condicao_uso.value,
            financiamento.renda_teto_familiar,
            financiamento.renda_minima_exigida,
            financiamento.valor_entrada,
            financiamento.valor_mensais,
            financiamento.qtde_mensais,
            financiamento.valor_intermediarias,
            financiamento.qtde_intermediarias,
            financiamento.valor_chaves,
            financiamento.valor_financiamento
        )

        cursor = self._db.cursor()
        cursor.execute(query, valores)
        self._db.commit()

        financiamento.id = cursor.lastrowid
        cursor.execute("SELECT created_at FROM tabelas_financiamento WHERE id = ?", (financiamento.id,))
        row = cursor.fetchone()
        if row:
            financiamento.created_at = row[0]

        return financiamento

    def buscar_por_unidade(self, unidade_id: int) -> Optional[TabelaFinanciamento]:
        """
        Busca o financiamento satélite associado a uma unidade (0 ou 1) mapeando de volta para a Entidade.
        """
        query = "SELECT * FROM tabelas_financiamento WHERE unidade_id = ?"
        cursor = self._db.cursor()
        cursor.execute(query, (unidade_id,))
        linha = cursor.fetchone()

        if not linha:
            return None

        entidade = TabelaFinanciamento(
            id=linha[0],
            unidade_id=linha[1],
            perfil_comprador=PerfilCompradorEnum(linha[2]),
            condicao_uso=CondicaoUsoEnum(linha[3]),
            renda_teto_familiar=linha[4],
            renda_minima_exigida=linha[5],
            valor_entrada=linha[6],
            valor_mensais=linha[7],
            qtde_mensais=linha[8],
            valor_intermediarias=linha[9],
            qtde_intermediarias=linha[10],
            valor_chaves=linha[11],
            valor_financiamento=linha[12],
            created_at=linha[13]
        )
        
        return entidade