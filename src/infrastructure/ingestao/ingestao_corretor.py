# ============================================================
# INGESTOR: IngestaoCorretor
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLSX de corretores e persiste no banco.
#            Pipeline: XLSParser → CorretorInputDTO → CorretorService
#
# Colunas esperadas (snake_case após XLSParser):
#   nome (obrigatório) | telefone | email | creci | observacoes
# ============================================================

import os
import shutil
from datetime import datetime

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser
from src.infrastructure.ingestao.normalizador import Normalizador
from src.application.corretor.services.corretor_service import CorretorService
from src.infrastructure.corretor.repositories.corretor_repository import CorretorRepository
from src.domain.corretor.dto.corretor_input_dto import CorretorInputDTO

PASTA_ENTRADA    = "data/entrada/corretor"
PASTA_PROCESSADO = "data/processado/corretor"
PASTA_ERROS      = "data/erros/corretor"


class IngestaoCorretor(BaseIngestor):
    """Ingestor de corretores a partir de arquivos XLSX."""

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.service = CorretorService(CorretorRepository(db_path))
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
        print(f"[IngestaoCorretor] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[CorretorInputDTO]:
        """Converte rows em CorretorInputDTOs normalizados.
        Pula linhas sem nome — campo obrigatório."""
        dtos = []
        for i, d in enumerate(dados, start=1):
            nome = self.norm.texto(d.get("nome"))
            if not nome:
                print(f"[IngestaoCorretor] ⚠️  Linha {i} ignorada: campo 'nome' ausente")
                continue

            dto = CorretorInputDTO(
                nome=nome,
                telefone=self.norm.limpar_telefone(d.get("telefone")),
                email=self.norm.texto(d.get("email")),
                creci=self.norm.texto(d.get("creci")),     # registro profissional
                observacoes=self.norm.texto(d.get("observacoes"))
            )
            dtos.append(dto)

        print(f"[IngestaoCorretor] {len(dtos)} corretor(es) válido(s) para ingestão")
        return dtos

    def salvar(self, dados: list[CorretorInputDTO]) -> list:
        """Persiste cada CorretorInputDTO via CorretorService."""
        resultados = []
        erros = 0
        for dto in dados:
            try:
                criado = self.service.cadastrar(dto)
                resultados.append(criado)
                print(f"[IngestaoCorretor] ✅ '{criado.nome}' salvo com ID {criado.id}")
            except Exception as e:
                erros += 1
                print(f"[IngestaoCorretor] ❌ Erro ao salvar '{dto.nome}': {e}")

        print(f"[IngestaoCorretor] Concluído: {len(resultados)} salvo(s), {erros} erro(s)")
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
            print("[IngestaoCorretor] Nenhum arquivo encontrado.")
            return

        for arquivo in arquivos:
            caminho = os.path.join(PASTA_ENTRADA, arquivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            nome_destino = f"{nome}_{timestamp}{ext}"

            print(f"\n[IngestaoCorretor] Processando: {arquivo}")
            try:
                self.executar(caminho)
                shutil.move(caminho, os.path.join(PASTA_PROCESSADO, nome_destino))
                print(f"[IngestaoCorretor] ✅ Movido para processado: {nome_destino}")
            except Exception as e:
                print(f"[IngestaoCorretor] ❌ Erro: {e}")
                shutil.move(caminho, os.path.join(PASTA_ERROS, nome_destino))
                print(f"[IngestaoCorretor] ⚠️  Movido para erros: {nome_destino}")


if __name__ == "__main__":
    IngestaoCorretor().executar_pasta()