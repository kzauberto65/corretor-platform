# arquivo: imobiliaria_service.py
from src.persistencia.repositorios.imobiliaria_repository import ImobiliariaRepository

class ImobiliariaService:
    def __init__(self):
        self.repo = ImobiliariaRepository()

    def criar_imobiliaria(self, nome, cnpj=None, contato=None, observacoes=None):
        if not nome or nome.strip() == "":
            raise ValueError("Nome da imobiliária é obrigatório")

        # Evitar duplicidade por nome
        existente_nome = self.repo.buscar_por_nome(nome)
        if existente_nome:
            return existente_nome

        # Evitar duplicidade por CNPJ (quando informado)
        if cnpj:
            existentes = self.repo.listar()
            for im in existentes:
                if im["cnpj"] and im["cnpj"] == cnpj:
                    return im

        # Criar imobiliária
        self.repo.criar(nome, cnpj, contato, observacoes)

        # Retornar a última inserida
        imobiliarias = self.repo.listar()
        return imobiliarias[-1] if imobiliarias else None

    def listar_imobiliarias(self):
        return self.repo.listar()

    def buscar_por_id(self, imobiliaria_id):
        return self.repo.buscar_por_id(imobiliaria_id)

    def atualizar_imobiliaria(self, imobiliaria_id, nome, cnpj=None, contato=None, observacoes=None):
        existente = self.repo.buscar_por_id(imobiliaria_id)
        if not existente:
            raise ValueError("Imobiliária não encontrada")

        if not nome or nome.strip() == "":
            raise ValueError("Nome da imobiliária é obrigatório")

        self.repo.atualizar(imobiliaria_id, nome, cnpj, contato, observacoes)

        return self.repo.buscar_por_id(imobiliaria_id)

    def remover_imobiliaria(self, imobiliaria_id):
        existente = self.repo.buscar_por_id(imobiliaria_id)
        if not existente:
            raise ValueError("Imobiliária não encontrada")

        self.repo.remover(imobiliaria_id)
        return True