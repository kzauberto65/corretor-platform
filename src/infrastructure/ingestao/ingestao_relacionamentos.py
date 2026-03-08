# ============================================================
# INGESTOR: IngestaoRelacionamentos
# Camada: infrastructure/ingestao/
# Descrição: Processa vínculos N:N entre entidades já cadastradas.
#            Não cria entidades — apenas relaciona IDs existentes.
#            Pipeline: list[dict] → validação → Service de relacionamento
#
# Tipos de relacionamento suportados:
#   construtora_imobiliaria → vincula construtora ↔ imobiliária
#   corretor_imobiliaria    → vincula corretor ↔ imobiliária
#   corretor_unidade        → vincula corretor ↔ unidade (Sprint 10.5)
#
# Formato esperado da lista de dicts:
#   [
#     {"tipo": "construtora_imobiliaria",
#      "construtora_id": 1, "imobiliaria_id": 2,
#      "tipo_parceria": "exclusiva"},
#     {"tipo": "corretor_imobiliaria",
#      "corretor_id": 3, "imobiliaria_id": 2},
#     {"tipo": "corretor_unidade",
#      "corretor_id": 3, "unidade_id": 10}
#   ]
# ============================================================

from src.infrastructure.ingestao.base_ingestor import BaseIngestor
from src.application.construtora_imobiliaria.services.construtora_imobiliaria_service import ConstrutoraImobiliariaService
from src.application.corretor_imobiliaria.services.corretor_imobiliaria_service import CorretorImobiliariaService
from src.application.corretor_unidade.services.corretor_unidade_service import CorretorUnidadeService
from src.infrastructure.construtora_imobiliaria.repositories.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository
from src.infrastructure.corretor_imobiliaria.repositories.corretor_imobiliaria_repository import CorretorImobiliariaRepository
from src.infrastructure.corretor_unidade.repositories.corretor_unidade_repository import CorretorUnidadeRepository
from src.domain.construtora_imobiliaria.dto.construtora_imobiliaria_input_dto import ConstrutoraImobiliariaInputDTO
from src.domain.corretor_imobiliaria.dto.corretor_imobiliaria_input_dto import CorretorImobiliariaInputDTO
from src.domain.corretor_unidade.dto.corretor_unidade_input_dto import CorretorUnidadeInputDTO

# Tipos de relacionamento válidos — qualquer outro será ignorado com aviso
TIPOS_VALIDOS = {"construtora_imobiliaria", "corretor_imobiliaria", "corretor_unidade"}


class IngestaoRelacionamentos(BaseIngestor):
    """Ingestor de relacionamentos N:N entre entidades.

    Não usa XLSParser — recebe lista de dicts diretamente,
    geralmente gerada pela IngestaoCentral ou por scripts de migração.
    """

    def __init__(self, db_path: str = "src/infrastructure/database/corretor.db"):
        self.ci_service = ConstrutoraImobiliariaService(ConstrutoraImobiliariaRepository(db_path))
        self.cori_service = CorretorImobiliariaService(CorretorImobiliariaRepository(db_path))
        self.coru_service = CorretorUnidadeService(CorretorUnidadeRepository(db_path))

    # ----------------------------------------------------------
    # PIPELINE: carregar → transformar → salvar
    # ----------------------------------------------------------

    def carregar(self, fonte: list[dict]) -> list[dict]:
        """Recebe lista de dicts diretamente — sem leitura de arquivo."""
        print(f"[IngestaoRelacionamentos] {len(fonte)} relacionamento(s) recebido(s)")
        return fonte

    def transformar(self, dados: list[dict]) -> list[dict]:
        """Valida campos obrigatórios por tipo de relacionamento.
        Pula itens inválidos com log de aviso."""
        validos = []
        for i, item in enumerate(dados, start=1):
            tipo = item.get("tipo")

            if tipo not in TIPOS_VALIDOS:
                print(f"[IngestaoRelacionamentos] ⚠️  Item {i} ignorado: "
                      f"tipo '{tipo}' inválido. Aceitos: {TIPOS_VALIDOS}")
                continue

            # Validação por tipo
            if tipo == "construtora_imobiliaria":
                if not item.get("construtora_id") or not item.get("imobiliaria_id"):
                    print(f"[IngestaoRelacionamentos] ⚠️  Item {i} ignorado: "
                          f"construtora_id e imobiliaria_id são obrigatórios")
                    continue

            elif tipo == "corretor_imobiliaria":
                if not item.get("corretor_id") or not item.get("imobiliaria_id"):
                    print(f"[IngestaoRelacionamentos] ⚠️  Item {i} ignorado: "
                          f"corretor_id e imobiliaria_id são obrigatórios")
                    continue

            elif tipo == "corretor_unidade":
                if not item.get("corretor_id") or not item.get("unidade_id"):
                    print(f"[IngestaoRelacionamentos] ⚠️  Item {i} ignorado: "
                          f"corretor_id e unidade_id são obrigatórios")
                    continue

            validos.append(item)

        print(f"[IngestaoRelacionamentos] {len(validos)} relacionamento(s) válido(s)")
        return validos

    def salvar(self, dados: list[dict]) -> list:
        """Persiste cada relacionamento via service correspondente."""
        resultados = []
        erros = 0

        for item in dados:
            tipo = item["tipo"]
            try:
                if tipo == "construtora_imobiliaria":
                    dto = ConstrutoraImobiliariaInputDTO(
                        construtora_id=item["construtora_id"],
                        imobiliaria_id=item["imobiliaria_id"],
                        tipo_parceria=item.get("tipo_parceria"),
                        observacoes=item.get("observacoes")
                    )
                    resultado = self.ci_service.cadastrar(dto)

                elif tipo == "corretor_imobiliaria":
                    dto = CorretorImobiliariaInputDTO(
                        corretor_id=item["corretor_id"],
                        imobiliaria_id=item["imobiliaria_id"],
                        tipo_vinculo=item.get("tipo_vinculo"),
                        observacoes=item.get("observacoes")
                    )
                    resultado = self.cori_service.cadastrar(dto)

                elif tipo == "corretor_unidade":
                    # Sprint 10.5 — corretor vinculado à unidade (não ao empreendimento)
                    dto = CorretorUnidadeInputDTO(
                        corretor_id=item["corretor_id"],
                        unidade_id=item["unidade_id"],
                        tipo_vinculo=item.get("tipo_vinculo"),
                        observacoes=item.get("observacoes")
                    )
                    resultado = self.coru_service.cadastrar(dto)

                resultados.append(resultado)
                print(f"[IngestaoRelacionamentos] ✅ {tipo} vinculado")

            except Exception as e:
                erros += 1
                print(f"[IngestaoRelacionamentos] ❌ Erro em {tipo}: {e}")

        print(f"\n[IngestaoRelacionamentos] Concluído: {len(resultados)} vínculo(s), {erros} erro(s)")
        return resultados