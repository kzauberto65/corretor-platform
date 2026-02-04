# arquivo: unidade_service.py
from src.persistencia.repositorios.unidade_repository import UnidadeRepository

class UnidadeService:
    def __init__(self):
        self.repo = UnidadeRepository()

    def criar_unidade(
        self,
        empreendimento_id,
        construtora_id,
        codigo_unidade,
        metragem,
        valor,
        observacoes=None,
        tipo_unidade_id=None
    ):
        # Apenas empreendimento_id é obrigatório
        if not empreendimento_id:
            raise ValueError("ID de empreendimento é obrigatório")

        # Código da unidade também é obrigatório
        if not codigo_unidade or codigo_unidade.strip() == "":
            raise ValueError("Código da unidade é obrigatório")

        # Evitar duplicidade por (empreendimento_id + codigo_unidade)
        existentes = self.repo.listar_por_empreendimento(empreendimento_id)
        for u in existentes:
            if u["codigo_unidade"].lower() == codigo_unidade.lower():
                return u  # já existe, retorna a existente

        # Criar unidade (construtora_id pode ser None)
        self.repo.criar(
            empreendimento_id,
            construtora_id,
            codigo_unidade,
            metragem,
            valor,
            observacoes,
            tipo_unidade_id
        )

        # Recuperar a última inserida
        unidades = self.repo.listar()
        return unidades[-1] if unidades else None

    def listar_unidades(self):
        return self.repo.listar()

    def listar_unidades_completas(self):
        """Retorna unidades com empreendimento, construtora e tipo."""
        return self.repo.listar_completo()

    def listar_por_empreendimento(self, empreendimento_id):
        return self.repo.listar_por_empreendimento(empreendimento_id)

    def buscar_unidade(self, unidade_id):
        return self.repo.buscar_por_id(unidade_id)

    def atualizar_unidade(
        self,
        unidade_id,
        codigo_unidade=None,
        metragem=None,
        valor=None,
        observacoes=None,
        tipo_unidade_id=None
    ):
        existente = self.repo.buscar_por_id(unidade_id)
        if not existente:
            raise ValueError("Unidade não encontrada")

        self.repo.atualizar(
            unidade_id,
            codigo_unidade,
            metragem,
            valor,
            observacoes,
            tipo_unidade_id
        )

        return self.repo.buscar_por_id(unidade_id)

    def remover_unidade(self, unidade_id):
        existente = self.repo.buscar_por_id(unidade_id)
        if not existente:
            raise ValueError("Unidade não encontrada")

        self.repo.remover(unidade_id)
        return True