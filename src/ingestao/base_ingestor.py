# src/ingestao/base_ingestor.py

class BaseIngestor:
    def carregar(self, fonte):
        raise NotImplementedError("Método carregar() deve ser implementado")

    def transformar(self, dados):
        raise NotImplementedError("Método transformar() deve ser implementado")

    def salvar(self, dados):
        raise NotImplementedError("Método salvar() deve ser implementado")

    def executar(self, fonte):
        dados = self.carregar(fonte)
        dados_transformados = self.transformar(dados)
        return self.salvar(dados_transformados)