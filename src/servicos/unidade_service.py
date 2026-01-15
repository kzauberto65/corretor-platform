from src.persistencia.repositorios.unidade_repository import UnidadeRepository

class UnidadeService:
    def __init__(self):
        self.repo = UnidadeRepository()

    def criar_unidade(
        self,
        imovel_id,
        construtora_id,
        codigo_unidade,
        metragem,
        valor,
        observacoes=None,
        unidade_referencia_id=None
    ):
        if not imovel_id or not construtora_id:
            raise ValueError("IDs de imóvel e construtora são obrigatórios")

        if not codigo_unidade or codigo_unidade.strip() == "":
            raise ValueError("Código da unidade é obrigatório")

        # Evitar duplicidade por (imovel_id + codigo_unidade)
        existentes = self.repo.listar_por_imovel(imovel_id)
        for u in existentes:
            if u["codigo_unidade"].lower() == codigo_unidade.lower():
                return u  # já existe, retorna a existente

        # Criar unidade com referência
        self.repo.criar(
            imovel_id,
            construtora_id,
            codigo_unidade,
            metragem,
            valor,
            observacoes,
            unidade_referencia_id
        )

        return self.repo.listar()[-1]  # retorna a última inserida

    def listar_unidades(self):
        return self.repo.listar()

    def listar_por_imovel(self, imovel_id):
        return self.repo.listar_por_imovel(imovel_id)

    def listar_por_construtora(self, construtora_id):
        return self.repo.listar_por_construtora(construtora_id)