from src.persistencia.repositorios.imovel_repository import ImovelRepository

class ImovelService:
    def __init__(self):
        self.repo = ImovelRepository()

    def criar_imovel(
        self,
        regiao,
        bairro,
        cidade,
        estado,
        produto,
        endereco=None,
        data_entrega=None,
        status_entrega=None,
        tipo=None,
        descricao=None
    ):
        if not regiao or not bairro or not cidade or not estado or not produto:
            raise ValueError("Campos obrigatórios do imóvel não foram preenchidos")

        # Evitar duplicidade por (bairro + produto + cidade)
        existentes = self.repo.listar()
        for im in existentes:
            if (
                im["bairro"].lower() == bairro.lower()
                and im["produto"].lower() == produto.lower()
                and im["cidade"].lower() == cidade.lower()
            ):
                return im  # já existe, retorna o existente

        self.repo.criar(
            regiao,
            bairro,
            cidade,
            estado,
            produto,
            endereco,
            data_entrega,
            status_entrega,
            tipo,
            descricao
        )

        return self.repo.listar()[-1]  # retorna o último inserido

    def listar_imoveis(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)