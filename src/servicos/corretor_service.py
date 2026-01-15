from src.persistencia.repositorios.corretor_repository import CorretorRepository

class CorretorService:
    def __init__(self):
        self.repo = CorretorRepository()

    def criar_corretor(self, nome, telefone=None, email=None, creci=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome do corretor é obrigatório")

        # Evitar duplicidade por nome + telefone
        existentes = self.repo.listar()
        for c in existentes:
            if c["nome"].lower() == nome.lower():
                if telefone and c["telefone"] == telefone:
                    return c  # já existe, retorna o existente

        self.repo.criar(nome, telefone, email, creci, observacoes)
        return self.repo.listar()[-1]  # retorna o último inserido

    def listar_corretores(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)