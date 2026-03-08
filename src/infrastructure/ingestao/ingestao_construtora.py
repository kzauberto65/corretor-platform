# ============================================================
# INGESTOR: IngestaoConstrutora
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLSX de construtoras e persiste no banco.
#            Pipeline: XLSParser → ConstrutoraInputDTO → ConstrutoraService
#
# Colunas esperadas (snake_case após XLSParser):
#   nome (obrigatório) | cnpj | contato | observacoes
# ============================================================

import os
import shutil
from datetime import datetime

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser
from src.infrastructure.ingestao.normalizador import Normalizador
from src.application.construtora.services.construtora_service import ConstrutoraService
from src.infrastructure.construtora.repositories.construtora_repository import ConstrutoraRepository
from src.domain.construtora.dto.construtora_input_dto import ConstrutoraInputDTO

PASTA_ENTRADA    = "data/entrada/construtora"
PASTA_PROCESSADO = "data/processado/construtora"
PASTA_ERROS      = "data/erros/construtora"


class IngestaoConstrutora(BaseIngestor):
    """Ingestor de construtoras a partir de arquivos XLSX."""

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.service = ConstrutoraService(ConstrutoraRepository(db_path))
        self.parser = XLSParser()
        self.norm = Normalizador()

    # ----------------------------------------------------------
    # PIPELINE: carregar → transformar → salvar
    # ----------------------------------------------------------

    def carregar(self, arquivo: str) -> list[dict]:
        """Lê XLSX via XLSParser e retorna rows brutas."""
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        rows = self.parser.parse(arquivo)
        print(f"[IngestaoConstrutora] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[ConstrutoraInputDTO]:
        """Converte rows em ConstrutoraInputDTOs.
        Pula linhas sem nome — campo obrigatório."""
        dtos = []
        for i, d in enumerate(dados, start=1):
            nome = self.norm.texto(d.get("nome"))
            if not nome:
                print(f"[IngestaoConstrutora] ⚠️  Linha {i} ignorada: campo 'nome' ausente")
                continue

            dto = ConstrutoraInputDTO(
                nome=nome,
                cnpj=self.norm.limpar_cnpj(d.get("cnpj")),
                contato=self.norm.texto(d.get("contato")),
                observacoes=self.norm.texto(d.get("observacoes")),
                fonte="ingestao_xlsx",
                data_registro=None,
                usuario_id=None,
                justificativa=None
            )
            dtos.append(dto)

        print(f"[IngestaoConstrutora] {len(dtos)} construtora(s) válida(s) para ingestão")
        return dtos

    def salvar(self, dados: list[ConstrutoraInputDTO]) -> list:
        """Persiste cada ConstrutoraInputDTO via ConstrutoraService."""
        resultados = []
        erros = 0
        for dto in dados:
            try:
                criado = self.service.cadastrar(dto)
                resultados.append(criado)
                print(f"[IngestaoConstrutora] ✅ '{criado.nome}' salva com ID {criado.id}")
            except Exception as e:
                erros += 1
                print(f"[IngestaoConstrutora] ❌ Erro ao salvar '{dto.nome}': {e}")

        print(f"[IngestaoConstrutora] Concluído: {len(resultados)} salva(s), {erros} erro(s)")
        return resultados

    # ----------------------------------------------------------
    # MODO PASTA
    # ----------------------------------------------------------

    def executar_pasta(self):
        """Processa todos os arquivos XLSX da pasta de entrada."""
        os.makedirs(PASTA_ENTRADA, exist_ok=True)
        os.makedirs(PASTA_PROCESSADO, exist_ok=True)
        os.makedirs(PASTA_ERROS, exist_ok=True)

        arquivos = [
            f for f in os.listdir(PASTA_ENTRADA)
            if f.lower().endswith((".xlsx", ".xls"))
        ]

        if not arquivos:
            print("[IngestaoConstrutora] Nenhum arquivo encontrado.")
            return

        for arquivo in arquivos:
            caminho = os.path.join(PASTA_ENTRADA, arquivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            nome_destino = f"{nome}_{timestamp}{ext}"

            print(f"\n[IngestaoConstrutora] Processando: {arquivo}")
            try:
                self.executar(caminho)
                shutil.move(caminho, os.path.join(PASTA_PROCESSADO, nome_destino))
                print(f"[IngestaoConstrutora] ✅ Movido para processado: {nome_destino}")
            except Exception as e:
                print(f"[IngestaoConstrutora] ❌ Erro: {e}")
                shutil.move(caminho, os.path.join(PASTA_ERROS, nome_destino))
                print(f"[IngestaoConstrutora] ⚠️  Movido para erros: {nome_destino}")


if __name__ == "__main__":
    IngestaoConstrutora().executar_pasta()