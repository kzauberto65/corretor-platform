# ============================================================
# BASE: BaseIngestor
# Camada: infrastructure/ingestao/
# Descrição: Contrato base para todos os ingestores do projeto.
#            Define o pipeline padrão: carregar → transformar → salvar.
#            Todo ingestor concreto deve herdar esta classe e
#            implementar os três métodos obrigatórios.
#
# Pipeline padrão:
#   XLSX → carregar() → list[dict] → transformar() → list[DTO]
#   → salvar() → list[resultado]
#
# Ingestores concretos:
#   IngestaoEmpreendimento, IngestaoUnidade, IngestaoLead,
#   IngestaoMailing, IngestaoCorretor, IngestaoConstrutora...
# ============================================================


class BaseIngestor:
    """Classe base para todos os ingestores.

    Define o contrato de três métodos que todo ingestor deve implementar.
    O método executar() orquestra o pipeline completo e não deve ser
    sobrescrito — apenas os três métodos abaixo.
    """

    def carregar(self, fonte: str) -> list[dict]:
        """Lê a fonte de dados (arquivo XLSX, dict, API) e retorna
        lista de dicts com os dados brutos.
        Deve validar existência do arquivo antes de processar."""
        raise NotImplementedError("carregar() deve ser implementado pelo ingestor concreto")

    def transformar(self, dados: list[dict]) -> list:
        """Converte dados brutos em DTOs tipados.
        Deve validar campos obrigatórios e pular linhas inválidas com log.
        Nunca deve quebrar o processo — erros por linha são logados."""
        raise NotImplementedError("transformar() deve ser implementado pelo ingestor concreto")

    def salvar(self, dados: list) -> list:
        """Persiste os DTOs via Service.
        Deve capturar erros por item e logar sem interromper o processo.
        Retorna lista dos registros salvos com sucesso."""
        raise NotImplementedError("salvar() deve ser implementado pelo ingestor concreto")

    def executar(self, fonte: str) -> list:
        """Orquestra o pipeline completo: carregar → transformar → salvar.
        Ponto de entrada principal — não sobrescrever nos ingestores concretos.
        Retorna lista dos registros salvos com sucesso."""
        dados = self.carregar(fonte)
        dados_transformados = self.transformar(dados)
        return self.salvar(dados_transformados)