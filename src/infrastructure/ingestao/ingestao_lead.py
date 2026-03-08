# ============================================================
# INGESTOR: IngestaoLead
# Camada: infrastructure/ingestao/
# Descrição: Lê arquivos XLSX da pasta data/entrada/lead,
#            persiste no banco e move para processado ou erros.
#            Pipeline: XLSParser → LeadInputDTO → LeadService
#
# Estrutura de pastas:
#   data/entrada/lead/    → arquivos aguardando ingestão
#   data/processado/lead/ → arquivos processados com sucesso
#   data/erros/lead/      → arquivos que falharam
#
# Colunas esperadas (snake_case após XLSParser):
#   nome | email | telefone | origem | tags | intencao |
#   tipo_imovel | preco_min | preco_max | quartos | vagas |
#   metragem_min | metragem_max | bairro_interesse |
#   regiao_interesse | cidade_interesse | urgencia | motivo |
#   utm_source | utm_medium | utm_campaign | canal_preferido
# ============================================================

import os
import shutil
from datetime import datetime

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser
from src.infrastructure.ingestao.normalizador import Normalizador
from src.application.lead.services.lead_service import LeadService
from src.infrastructure.lead.repositories.lead_repository import LeadRepository
from src.domain.lead.dto.lead_input_dto import LeadInputDTO

PASTA_ENTRADA    = "data/entrada/lead"
PASTA_PROCESSADO = "data/processado/lead"
PASTA_ERROS      = "data/erros/lead"


class IngestaoLead(BaseIngestor):
    """Ingestor de leads a partir de arquivos XLSX.

    Suporta dois modos:
    1. executar(arquivo) — processa um arquivo específico
    2. executar_pasta()  — processa todos os arquivos da pasta de entrada
    """

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.service = LeadService(LeadRepository(db_path))
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
        print(f"[IngestaoLead] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[LeadInputDTO]:
        """Converte rows em LeadInputDTOs normalizados.
        Pula linhas sem email E sem telefone — contato mínimo obrigatório."""
        dtos = []
        for i, d in enumerate(dados, start=1):
            email = self.norm.texto(d.get("email"))
            telefone = self.norm.limpar_telefone(d.get("telefone"))

            if not email and not telefone:
                print(f"[IngestaoLead] ⚠️  Linha {i} ignorada: sem email nem telefone")
                continue

            dto = LeadInputDTO(
                # Identificação
                nome=self.norm.texto(d.get("nome")),
                email=email,
                telefone=telefone,
                origem=self.norm.texto(d.get("origem")),
                tags=self.norm.texto(d.get("tags")),

                # Status
                status=self.norm.texto(d.get("status")) or "novo",

                # Intenção imobiliária
                intencao=self.norm.texto(d.get("intencao")),
                tipo_imovel=self.norm.texto(d.get("tipo_imovel")),
                faixa_preco=self.norm.texto(d.get("faixa_preco")),
                preco_min=self.norm.moeda(d.get("preco_min")),
                preco_max=self.norm.moeda(d.get("preco_max")),
                quartos=self.norm.inteiro(d.get("quartos")),
                vagas=self.norm.inteiro(d.get("vagas")),
                metragem_min=self.norm.flutuante(d.get("metragem_min")),
                metragem_max=self.norm.flutuante(d.get("metragem_max")),

                # Localização de interesse — normalizar antes de usar no IAEngine
                bairro_interesse=self.norm.texto(d.get("bairro_interesse")),
                regiao_interesse=self.norm.texto(d.get("regiao_interesse")),
                cidade_interesse=self.norm.texto(d.get("cidade_interesse")),

                # Qualificação
                urgencia=self.norm.texto(d.get("urgencia")),
                motivo=self.norm.texto(d.get("motivo")),

                # Marketing
                utm_source=self.norm.texto(d.get("utm_source")),
                utm_medium=self.norm.texto(d.get("utm_medium")),
                utm_campaign=self.norm.texto(d.get("utm_campaign")),
                utm_term=self.norm.texto(d.get("utm_term")),
                utm_content=self.norm.texto(d.get("utm_content")),
                canal_preferido=self.norm.texto(d.get("canal_preferido")),

                # Enriquecimento
                data_ingestao=self.norm.data(d.get("data_ingestao")),
                profile_json=self.norm.texto(d.get("profile_json")),
                historico_json=None,
                score_lead=self.norm.flutuante(d.get("score_lead")),
            )
            dtos.append(dto)

        print(f"[IngestaoLead] {len(dtos)} lead(s) válido(s) para ingestão")
        return dtos

    def salvar(self, dados: list[LeadInputDTO]) -> list:
        """Persiste cada LeadInputDTO via LeadService."""
        resultados = []
        erros = 0
        for dto in dados:
            try:
                criado = self.service.cadastrar(dto)
                resultados.append(criado)
            except Exception as e:
                erros += 1
                print(f"[IngestaoLead] ❌ Erro ao salvar '{dto.email or dto.telefone}': {e}")

        print(f"[IngestaoLead] Concluído: {len(resultados)} salvo(s), {erros} erro(s)")
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
            print("[IngestaoLead] Nenhum arquivo encontrado em data/entrada/lead/")
            return

        for arquivo in arquivos:
            caminho = os.path.join(PASTA_ENTRADA, arquivo)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome, ext = os.path.splitext(arquivo)
            nome_destino = f"{nome}_{timestamp}{ext}"

            print(f"\n[IngestaoLead] Processando: {arquivo}")
            try:
                self.executar(caminho)
                shutil.move(caminho, os.path.join(PASTA_PROCESSADO, nome_destino))
                print(f"[IngestaoLead] ✅ Movido para processado: {nome_destino}")
            except Exception as e:
                print(f"[IngestaoLead] ❌ Erro: {e}")
                shutil.move(caminho, os.path.join(PASTA_ERROS, nome_destino))
                print(f"[IngestaoLead] ⚠️  Movido para erros: {nome_destino}")


if __name__ == "__main__":
    IngestaoLead().executar_pasta()