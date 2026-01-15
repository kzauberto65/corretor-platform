from src.persistencia.repositorios.corretor_imobiliaria_repository import CorretorImobiliariaRepository

class CorretorImobiliariaService:
    def __init__(self):
        self.repo = CorretorImobiliariaRepository()

    def vincular(self, corretor_id, imobiliaria_id):
        if not corretor_id or not imobiliaria_id:
            raise ValueError("IDs de corretor e imobiliária são obrigatórios")

        # Evitar duplicidade
        existentes = self.repo.listar_por_corretor(corretor_id)
        for rel in existentes:
            if rel["imobiliaria_id"] == imobiliaria_id:
                return rel  # já existe

        self.repo.criar(corretor_id, imobiliaria_id)
        return self.repo.listar()[-1]

    def listar(self):
        return self.repo.listar()

    def listar_por_corretor(self, corretor_id):
        return self.repo.listar_por_corretor(corretor_id)

    def listar_por_imobiliaria(self, imobiliaria_id):
        return self.repo.listar_por_imobiliaria(imobiliaria_id)