from src.persistencia.repositorios.construtora_imobiliaria_repository import ConstrutoraImobiliariaRepository

class ConstrutoraImobiliariaService:
    def __init__(self):
        self.repo = ConstrutoraImobiliariaRepository()

    def vincular(self, construtora_id, imobiliaria_id):
        if not construtora_id or not imobiliaria_id:
            raise ValueError("IDs de construtora e imobiliária são obrigatórios")

        # Evitar duplicidade
        existentes = self.repo.listar_por_construtora(construtora_id)
        for rel in existentes:
            if rel["imobiliaria_id"] == imobiliaria_id:
                return rel  # já existe

        self.repo.criar(construtora_id, imobiliaria_id)
        return self.repo.listar()[-1]

    def listar(self):
        return self.repo.listar()

    def listar_por_construtora(self, construtora_id):
        return self.repo.listar_por_construtora(construtora_id)

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.repo.listar_por_imobiliaria(imobiliaria_id)