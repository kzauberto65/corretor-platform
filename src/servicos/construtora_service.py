from src.persistencia.repositorios.construtora_repository import ConstrutoraRepository

class ConstrutoraService:
    def __init__(self):
        self.repo = ConstrutoraRepository()

    def criar_construtora(self, nome, cnpj=None, contato=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome da construtora é obrigatório")

        # Evitar duplicidade
        existentes = self.repo.listar()
        for c in existentes:
            if c["nome"].lower() == nome.lower():
                return c  # já existe, retorna a existente

        self.repo.criar(nome, cnpj, contato, observacoes)
        return self.repo.listar()[-1]  # retorna a última inserida

    def listar_construtoras(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)