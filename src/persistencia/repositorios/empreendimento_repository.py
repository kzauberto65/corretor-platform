from src.persistencia.repositorios.base_repository import BaseRepository

class EmpreendimentoRepository(BaseRepository):

    def criar(
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
        query = """
        INSERT INTO empreendimentos (
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            query,
            (
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
        )

    def listar(self):
        return self.fetch_all("SELECT * FROM empreendimentos")

    def buscar_por_id(self, empreendimento_id):
        return self.fetch_one(
            "SELECT * FROM empreendimentos WHERE id = ?",
            (empreendimento_id,)
        )

    def buscar_por_nome(self, nome):
        return self.fetch_one(
            "SELECT * FROM empreendimentos WHERE LOWER(nome) = LOWER(?)",
            (nome,)
        )

    def buscar_por_cidade(self, cidade):
        return self.fetch_all(
            "SELECT * FROM empreendimentos WHERE LOWER(cidade) = LOWER(?)",
            (cidade,)
        )

    def atualizar(
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
        query = """
        UPDATE empreendimentos
        SET
            nome = ?,
            regiao = ?,
            bairro = ?,
            cidade = ?,
            estado = ?,
            produto = ?,
            endereco = ?,
            tipologia = ?,
            data_entrega = ?,
            status_entrega = ?,
            tipo = ?,
            descricao = ?,
            periodo_lancamento = ?,
            unidade_referencia_id = ?,
            preco = ?,
            spe_id = ?,
            incorporadora_id = ?,
            proprietario_id = ?
        WHERE id = ?
        """
        self.execute(
            query,
            (
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
                proprietario_id,
                empreendimento_id
            )
        )

    def remover(self, empreendimento_id):
        self.execute(
            "DELETE FROM empreendimentos WHERE id = ?",
            (empreendimento_id,)
        )