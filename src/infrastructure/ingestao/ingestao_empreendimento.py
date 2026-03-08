# ============================================================
# INGESTOR: IngestaoEmpreendimento
# Camada: infrastructure/ingestao/
# Descrição: Lê planilhas XLSX de empreendimentos e persiste
#            no banco seguindo o pipeline padrão do projeto:
#            XLSX → XLSParser → rows → EmpreendimentoInputDTO →
#            EmpreendimentoService → banco
#
# Colunas esperadas na planilha (nome é obrigatório):
#   nome | regiao | bairro | cidade | estado | endereco |
#   produto | tipo | descricao | periodo_lancamento |
#   data_entrega | status_entrega | total_unidades |
#   amenities | padrao_construtivo |
#   incorporadora_id | proprietario_id | spe_id
#
# Uso direto:
#   ingestor = IngestaoEmpreendimento()
#   ingestor.executar("data/entrada/empreendimentos.xlsx")
# Sprint: 10.5 — alinhado ao novo schema e arquitetura
# ============================================================

import os
from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.infrastructure.ingestao.xls_parser import XLSParser
from src.application.empreendimento.services.empreendimento_service import EmpreendimentoService
from src.application.empreendimento.normalizers.empreendimento_normalizer import EmpreendimentoNormalizer
from src.infrastructure.empreendimento.repositories.empreendimento_repository import EmpreendimentoRepository
from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO


class IngestaoEmpreendimento(BaseIngestor):
    """Ingestor de empreendimentos a partir de planilhas XLSX.

    Segue o contrato do BaseIngestor:
      carregar() → transformar() → salvar()

    A normalização de dados brutos é delegada ao EmpreendimentoNormalizer
    dentro do Service — o ingestor apenas extrai e monta os DTOs.

    CAMPOS REMOVIDOS NA SPRINT 10.5 — NÃO MAPEAR:
      preco, tipologia, metragem_min, metragem_max → agora em unidades
    """

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        # Service com repository — único ponto de acesso ao banco
        self.service = EmpreendimentoService(EmpreendimentoRepository(db_path))
        self.parser = XLSParser()

    # ----------------------------------------------------------
    # PIPELINE: carregar → transformar → salvar
    # ----------------------------------------------------------

    def carregar(self, arquivo: str) -> list[dict]:
        """Lê o arquivo XLSX e retorna lista de dicts (rows brutas).
        Delega ao XLSParser — padrão do projeto."""
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
        rows = self.parser.parse(arquivo)
        print(f"[IngestaoEmpreendimento] {len(rows)} linha(s) lida(s) de '{arquivo}'")
        return rows

    def transformar(self, dados: list[dict]) -> list[EmpreendimentoInputDTO]:
        """Converte rows brutas em EmpreendimentoInputDTOs.
        Valida campo obrigatório nome.
        Linhas inválidas são puladas com log de aviso."""
        dtos = []
        for i, row in enumerate(dados, start=1):
            nome = self._extrair_str(row, "nome")
            if not nome:
                # nome é o campo mínimo de identificação do empreendimento
                print(f"[IngestaoEmpreendimento] ⚠️  Linha {i} ignorada: campo 'nome' ausente")
                continue

            dto = EmpreendimentoInputDTO(
                nome=nome,
                regiao=self._extrair_str(row, "regiao"),
                bairro=self._extrair_str(row, "bairro"),
                cidade=self._extrair_str(row, "cidade"),
                estado=self._extrair_str(row, "estado"),
                endereco=self._extrair_str(row, "endereco"),
                produto=self._extrair_str(row, "produto"),
                tipo=self._extrair_str(row, "tipo"),
                descricao=self._extrair_str(row, "descricao"),
                periodo_lancamento=self._extrair_str(row, "periodo_lancamento"),
                data_entrega=self._extrair_str(row, "data_entrega"),
                status_entrega=self._extrair_str(row, "status_entrega"),
                total_unidades=self._extrair_int(row, "total_unidades"),
                amenities=self._extrair_str(row, "amenities"),
                padrao_construtivo=self._extrair_str(row, "padrao_construtivo"),
                incorporadora_id=self._extrair_int(row, "incorporadora_id"),
                proprietario_id=self._extrair_int(row, "proprietario_id"),
                spe_id=self._extrair_int(row, "spe_id"),
                unidade_referencia_id=self._extrair_int(row, "unidade_referencia_id")

                # CAMPOS NÃO MAPEADOS — removidos na Sprint 10.5:
                # preco, tipologia, metragem_min, metragem_max → agora em unidades
            )
            dtos.append(dto)

        print(f"[IngestaoEmpreendimento] {len(dtos)} empreendimento(s) válido(s) para ingestão")
        return dtos

    def salvar(self, dtos: list[EmpreendimentoInputDTO]) -> list:
        """Persiste cada EmpreendimentoInputDTO via EmpreendimentoService.
        O Service chama o Normalizer internamente antes de salvar.
        Erros por linha são logados mas não interrompem o processo."""
        resultados = []
        erros = 0

        for dto in dtos:
            try:
                criado = self.service.cadastrar(dto)
                resultados.append(criado)
                print(f"[IngestaoEmpreendimento] ✅ '{criado.nome}' "
                      f"({criado.cidade}/{criado.estado}) salvo com ID {criado.id}")
            except Exception as e:
                erros += 1
                print(f"[IngestaoEmpreendimento] ❌ Erro ao salvar '{dto.nome}': {e}")

        print(f"\n[IngestaoEmpreendimento] Concluído: {len(resultados)} salvo(s), {erros} erro(s)")
        return resultados

    def executar(self, arquivo: str) -> list:
        """Executa o pipeline completo: carregar → transformar → salvar.
        Ponto de entrada principal do ingestor."""
        rows = self.carregar(arquivo)
        dtos = self.transformar(rows)
        return self.salvar(dtos)

    # ----------------------------------------------------------
    # HELPERS PRIVADOS DE EXTRAÇÃO
    # ----------------------------------------------------------

    def _extrair_str(self, row: dict, campo: str) -> str | None:
        """Extrai campo como string limpa. Retorna None se ausente."""
        val = row.get(campo)
        if val is None or str(val).strip() == "":
            return None
        return str(val).strip()

    def _extrair_float(self, row: dict, campo: str) -> float | None:
        """Extrai campo como float. Retorna None se inválido."""
        val = row.get(campo)
        if val is None:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def _extrair_int(self, row: dict, campo: str) -> int | None:
        """Extrai campo como int. Retorna None se inválido.
        Usa float() primeiro para aceitar '3.0' vindo de planilha."""
        val = row.get(campo)
        if val is None:
            return None
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return None