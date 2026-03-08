# ============================================================
# INGESTOR: IngestaoImobiliaria
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLSX de imobiliárias e persiste no banco.
#            Pipeline: XLSParser → ImobiliariaInputDTO → ImobiliariaService
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
from src.application.imobiliaria.services.imobiliaria_service import ImobiliariaService
from src.infrastructure.imobiliaria.repositories.imobiliaria_repository import ImobiliariaRepository
from src.domain.imobiliaria.dto.imobiliaria_input_dto import ImobiliariaInputDTO

PASTA_ENTRADA    = "data/entrada/imobiliaria"
PASTA_PROCESSADO = "data/processado/imobiliaria"
PASTA_ERROS      = "data/erros/imobiliaria"


class IngestaoImobiliaria(BaseIngestor):
    """Ingestor de imobiliárias a partir de arquivos XLSX."""

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.service = ImobiliariaService(ImobiliariaRepository(db_path))
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
        print(f"[IngestaoImobiliaria] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[ImobiliariaInputDTO]:
        """Converte rows em ImobiliariaInputDTOs.
        Pula linhas sem nome — campo obrigatório."""
        dtos = []
        for i, d in enumerate(dados, start=1):
            nome = self.norm.texto(d.get("nome"))
            if not nome:
                print(f"[IngestaoImobiliaria] ⚠️  Linha {i} ignorada: campo 'nome' ausente")
                continue

            dto = ImobiliariaInputDTO(
                nome=nome,
                cnpj=self.norm.limpar_cnpj(d.get("cnpj")),
                contato=self.norm.texto(d.get("contato")),
                observacoes=self.norm.texto(d.get("observacoes"))
            )
            dtos.append(dto)

        print(f"[IngestaoImobiliaria] {len(dtos)} imobiliária(s) válida(s) para ingestão")
        return dtos

    def salvar(self, dados: list[ImobiliariaInputDTO]) -> list:
        """Persiste cada ImobiliariaInputDTO via ImobiliariaService."""
        resultados = []
        erros = 0
        for dto in dados:
            try:
                criado = self.service.cadastrar(dto)
                resultados.append(criado)
                print(f"[IngestaoImobiliaria] ✅ '{criado.nome}' salva com ID {criado.id}")
            except Exception as e:
                erros += 1
                print(f"[IngestaoImobiliaria] ❌ Erro ao salvar '{dto.nome}': {e}")

        print(f"[IngestaoImobiliaria] Concluído: {len(resultados)} salva(s), {erros} erro(s)")
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
            print("[IngestaoImobiliaria] Nenhum arquivo encontrado.")
            return

        for arquivo in arquivos:
            caminho = os.path.join(PASTA_ENTRADA, arquivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            nome_destino = f"{nome}_{timestamp}{ext}"

            print(f"\n[IngestaoImobiliaria] Processando: {arquivo}")
            try:
                self.executar(caminho)
                shutil.move(caminho, os.path.join(PASTA_PROCESSADO, nome_destino))
                print(f"[IngestaoImobiliaria] ✅ Movido para processado: {nome_destino}")
            except Exception as e:
                print(f"[IngestaoImobiliaria] ❌ Erro: {e}")
                shutil.move(caminho, os.path.join(PASTA_ERROS, nome_destino))
                print(f"[IngestaoImobiliaria] ⚠️  Movido para erros: {nome_destino}")


if __name__ == "__main__":
    IngestaoImobiliaria().executar_pasta()