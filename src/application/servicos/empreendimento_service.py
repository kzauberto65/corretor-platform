from src.persistencia.repositorios.empreendimento_repository import EmpreendimentoRepository

class EmpreendimentoService:
    def __init__(self):
        self.repo = EmpreendimentoRepository()

    def criar_empreendimento(
        self,
        nome,
        regiao,
        bairro,
        cidade,
        estado,
        produto,
        endereco=None,
        tipologia=None,
        data_entrega=None,
        status_entrega=None,
        tipo=None,
        descricao=None,
        periodo_lancamento=None,
        unidade_referencia_id=None,
        preco=None,
        spe_id=None,
        incorporadora_id=None,
        proprietario_id=None
    ):
        # Validação dos campos obrigatórios
        if not nome or not cidade or not estado or not produto:
            raise ValueError("Campos obrigatórios do empreendimento não foram preenchidos")

        # Evitar duplicidade por nome
        existente = self.repo.buscar_por_nome(nome)
        if existente:
            return existente

        # Criar empreendimento
        self.repo.criar(
            nome,
            regiao,
            bairro,
            cidade,
            estado,
            produto,
            endereco,
            tipologia,
            data_entrega,
            status_entrega,
            tipo,
            descricao,
            periodo_lancamento,
            unidade_referencia_id,
            preco,
            spe_id,
            incorporadora_id,
            proprietario_id
        )

        # Retornar o último inserido
        empreendimentos = self.repo.listar()
        return empreendimentos[-1] if empreendimentos else None

    def listar_empreendimentos(self):
        return self.repo.listar()

    def buscar_por_id(self, empreendimento_id):
        return self.repo.buscar_por_id(empreendimento_id)

    def atualizar_empreendimento(
        self,
        empreendimento_id,
        nome,
        regiao,
        bairro,
        cidade,
        estado,
        produto,
        endereco=None,
        tipologia=None,
        data_entrega=None,
        status_entrega=None,
        tipo=None,
        descricao=None,
        periodo_lancamento=None,
        unidade_referencia_id=None,
        preco=None,
        spe_id=None,
        incorporadora_id=None,
        proprietario_id=None
    ):
        existente = self.repo.buscar_por_id(empreendimento_id)
        if not existente:
            raise ValueError("Empreendimento não encontrado")

        self.repo.atualizar(
            empreendimento_id,
            nome,
            regiao,
            bairro,
            cidade,
            estado,
            produto,
            endereco,
            tipologia,
            data_entrega,
            status_entrega,
            tipo,
            descricao,
            periodo_lancamento,
            unidade_referencia_id,
            preco,
            spe_id,
            incorporadora_id,
            proprietario_id
        )

        return self.repo.buscar_por_id(empreendimento_id)

    def remover_empreendimento(self, empreendimento_id):
        existente = self.repo.buscar_por_id(empreendimento_id)
        if not existente:
            raise ValueError("Empreendimento não encontrado")

        self.repo.remover(empreendimento_id)
        return True