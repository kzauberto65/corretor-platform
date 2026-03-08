# ============================================================
# INGESTOR: IngestaoUnidade
# Camada: infrastructure/ingestao/
# Descrição: Lê planilhas XLSX de unidades da pasta de entrada
#            e persiste Unidade E Financiamento automaticamente.
#            Move para "processado" ou "erros" ao final.
# ============================================================

import os
import shutil
from datetime import datetime
from typing import Tuple

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser

# --- Domínio: Unidade ---
from src.application.unidade.services.unidade_service import UnidadeService
from src.infrastructure.unidade.repositories.unidade_repository import UnidadeRepository
from src.domain.unidade.dto.unidade_input_dto import UnidadeInputDTO

# --- Domínio: Financiamento ---
from src.domain.financiamento.dto.tabela_financiamento_dto import TabelaFinanciamentoInputDTO
from src.application.financiamento.services.financiamento_service import FinanciamentoService
from src.infrastructure.financiamento.repositories.financiamento_repository import FinanciamentoRepositorySQLite


class IngestaoUnidade(BaseIngestor):
    """Ingestor de unidades a partir de planilhas XLSX.

    Segue o contrato do BaseIngestor:
      carregar() → transformar() → salvar()
    """

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.unidade_service = UnidadeService(UnidadeRepository(db_path))
        # Corrigido para instanciar a classe exata: FinanciamentoRepositorySQLite
        self.financiamento_service = FinanciamentoService(FinanciamentoRepositorySQLite(db_path))
        
        self.parser = XLSParser()

    # ----------------------------------------------------------
    # PIPELINE: carregar → transformar → salvar
    # ----------------------------------------------------------

    def carregar(self, arquivo: str) -> list[dict]:
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        rows = self.parser.parse(arquivo)
        print(f"[IngestaoUnidade] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[Tuple[UnidadeInputDTO, str]]:
        dtos_e_financiamentos: list[Tuple[UnidadeInputDTO, str]] = []
        for i, row in enumerate(dados, start=1):
            empreendimento_id = self._extrair_int(row, "empreendimento_id")
            if not empreendimento_id:
                print(f"[IngestaoUnidade] ⚠️ Linha {i} ignorada: empreendimento_id ausente")
                continue

            dto_unid = UnidadeInputDTO(
                empreendimento_id=empreendimento_id,
                codigo_unidade=self._extrair_str(row, "codigo_unidade"),
                preco=self._extrair_float(row, "preco"),
                metragem=self._extrair_float(row, "metragem"),
                dormitorios=self._extrair_int(row, "dormitorios"),
                suites=self._extrair_int(row, "suites"),
                vagas=self._extrair_int(row, "vagas"),
                tipo_unidade=self._extrair_str(row, "tipo_unidade"),
                andar=self._extrair_int(row, "andar"),
                disponibilidade=self._extrair_str(row, "disponibilidade"),
                descricao_unidade=self._extrair_str(row, "descricao_unidade"),
                observacoes=self._extrair_str(row, "observacoes")
            )
            
            tipo_financiamento = self._extrair_str(row, "tipo_financiamento") or "Outros"
            dtos_e_financiamentos.append((dto_unid, tipo_financiamento))

        print(f"[IngestaoUnidade] {len(dtos_e_financiamentos)} unidade(s) pronta(s) para ingestão cruzada")
        return dtos_e_financiamentos

    def salvar(self, dtos_com_financiamento: list[Tuple[UnidadeInputDTO, str]]) -> list:
        resultados = []
        erros = 0

        for dto_unid, tipo_financiamento in dtos_com_financiamento:
            try:
                # 1. SALVAR UNIDADE
                unidade_criada = self.unidade_service.cadastrar(dto_unid)
                pre_calc = dto_unid.preco or 0.0

                # 2. SALVAR FINANCIAMENTO VINCULADO
                condicao = "moradia_propria" if tipo_financiamento in ["HIS", "HMP"] else "Outros"

                dto_financiamento = TabelaFinanciamentoInputDTO(
                    unidade_id=unidade_criada.id,
                    perfil_comprador=tipo_financiamento,
                    condicao_uso=condicao,
                    valor_entrada=pre_calc * 0.10,
                    valor_mensais=(pre_calc * 0.20) / 36,
                    qtde_mensais=36,
                    valor_intermediarias=(pre_calc * 0.10) / 3,
                    qtde_intermediarias=3,
                    valor_chaves=pre_calc * 0.10,
                    valor_financiamento=pre_calc * 0.50,
                    renda_minima_exigida=None,
                    renda_teto_familiar=None
                )
                
                self.financiamento_service.cadastrar(dto_financiamento)
                resultados.append(unidade_criada)
                
            except Exception as e:
                erros += 1
                print(f"[IngestaoUnidade] ❌ Erro (empr. {dto_unid.empreendimento_id} / unid. {dto_unid.codigo_unidade}): {e}")

        print(f"\n[IngestaoUnidade] Concluído: {len(resultados)} criada(s), {erros} erro(s)")
        return resultados

    def executar(self, arquivo: str) -> list:
        """Executa um arquivo único e move para a pasta correspondente."""
        try:
            rows = self.carregar(arquivo)
            dtos = self.transformar(rows)

            if not dtos:
                print(f"[IngestaoUnidade] Nenhum dado válido em {arquivo}. Movendo para erros.")
                self._mover_arquivo(arquivo, "data/erros/unidades")
                return []

            resultados = self.salvar(dtos)

            if len(resultados) == len(dtos):
                self._mover_arquivo(arquivo, "data/processado/unidades")
            else:
                self._mover_arquivo(arquivo, "data/erros/unidades")

            return resultados

        except Exception as e:
            print(f"[IngestaoUnidade] ❌ Erro fatal na execução do arquivo {arquivo}: {e}")
            if os.path.exists(arquivo):
                self._mover_arquivo(arquivo, "data/erros/unidades")
            raise e

    # ----------------------------------------------------------
    # FILE MANAGEMENT (Mover Arquivo)
    # ----------------------------------------------------------

    def _mover_arquivo(self, arquivo_origem: str, diretorio_destino: str):
        try:
            os.makedirs(diretorio_destino, exist_ok=True)
            nome_arquivo = os.path.basename(arquivo_origem)
            nome_base, extensao = os.path.splitext(nome_arquivo)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            novo_nome = f"{nome_base}_{timestamp}{extensao}"
            caminho_destino = os.path.join(diretorio_destino, novo_nome)
            
            shutil.move(arquivo_origem, caminho_destino)
            print(f"[IngestaoUnidade] 📁 Arquivo movido para: {caminho_destino}")
            
        except Exception as e:
            print(f"[IngestaoUnidade] ⚠️ Falha ao mover arquivo '{arquivo_origem}': {e}")

    # ----------------------------------------------------------
    # HELPERS
    # ----------------------------------------------------------

    def _extrair_str(self, row: dict, campo: str) -> str | None:
        val = row.get(campo)
        if val is None or str(val).strip() == "": return None
        return str(val).strip()

    def _extrair_float(self, row: dict, campo: str) -> float | None:
        val = row.get(campo)
        if val is None: return None
        try: return float(val)
        except (ValueError, TypeError): return None

    def _extrair_int(self, row: dict, campo: str) -> int | None:
        val = row.get(campo)
        if val is None: return None
        try: return int(float(val))
        except (ValueError, TypeError): return None


# ==========================================================
# EXECUÇÃO AUTOMÁTICA (Usado pelo Menu)
# Varre a pasta de entrada e processa tudo que for XLSX
# ==========================================================
if __name__ == "__main__":
    pasta_entrada = os.path.join("data", "entrada", "unidades")
    
    # Cria a pasta caso não exista
    if not os.path.exists(pasta_entrada):
        os.makedirs(pasta_entrada, exist_ok=True)
        print(f"[IngestaoUnidade] Pasta '{pasta_entrada}' criada. Nenhuma planilha encontrada.")
    else:
        # Busca todos os XLSX na pasta de entrada
        arquivos_xlsx = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(".xlsx")]
        
        if not arquivos_xlsx:
            print(f"[IngestaoUnidade] Nenhuma planilha modelo encontrada em '{pasta_entrada}'.")
        else:
            ingestor = IngestaoUnidade()
            for arquivo in arquivos_xlsx:
                caminho_completo = os.path.join(pasta_entrada, arquivo)
                print(f"\n[IngestaoUnidade] ================= PROCESSANDO: {arquivo} =================")
                ingestor.executar(caminho_completo)