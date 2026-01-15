from src.persistencia.repositorios.imobiliaria_repository import ImobiliariaRepository

class ImobiliariaService:
    def __init__(self):
        self.repo = ImobiliariaRepository()

    def criar_imobiliaria(self, nome, cnpj=None, contato=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome da imobiliária é obrigatório")

        # Evitar duplicidade
        existentes = self.repo.listar()
        for i in existentes:
            if i["nome"].lower() == nome.lower():
                return i  # já existe, retorna a existente

        self.repo.criar(nome, cnpj, contato, observacoes)
        return self.repo.listar()[-1]  # retorna a última inserida

    def listar_imobiliarias(self):
        return self.repo.listar()

    def buscar_por_id(self, id):
        return self.repo.buscar_por_id(id)