from src.domain.empreendimento.dto.empreendimento_input_dto import EmpreendimentoInputDTO
from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO
from src.application.empreendimento.normalizers.empreendimento_normalizer import EmpreendimentoNormalizer
from src.domain.empreendimento.entities.empreendimento_entity import EmpreendimentoEntity

class EmpreendimentoService:

    def __init__(self, repo):
        self.repo = repo

    # ---------------------------------------------------------
    # CADASTRAR
    # ---------------------------------------------------------
    def cadastrar(self, input_dto: EmpreendimentoInputDTO) -> EmpreendimentoDTO:
        normalized = EmpreendimentoNormalizer.normalize(input_dto)

        data = normalized.__dict__.copy()
        data.pop("id", None)

        entity = EmpreendimentoEntity(id=None, **data)
        dto = EmpreendimentoDTO(**entity.to_dict())
        return self.repo.save(dto)

    # ---------------------------------------------------------
    # ATUALIZAR
    # ---------------------------------------------------------
    def atualizar(self, id: int, input_dto: EmpreendimentoInputDTO):
        existente = self.repo.find_by_id(id)
        if not existente:
            return None

        normalized = EmpreendimentoNormalizer.normalize(input_dto)

        data = normalized.__dict__.copy()
        data["id"] = id

        atualizado = EmpreendimentoDTO(**data)
        return self.repo.update(atualizado)

    # ---------------------------------------------------------
    # CONSULTAR COM FILTROS (AGORA COM METRAGEM)
    # ---------------------------------------------------------
    def consultar(
        self,
        cidade=None,
        regiao=None,
        metragem_min=None,
        metragem_max=None,
        lancamento=None,
        status=None,
        preco_min=None,
        preco_max=None,
        ordenar_por=None,
        ordem="asc"
    ):
        return self.repo.find_filtered(
            cidade=cidade,
            regiao=regiao,
            metragem_min=metragem_min,
            metragem_max=metragem_max,
            lancamento=lancamento,
            status=status,
            preco_min=preco_min,
            preco_max=preco_max,
            ordenar_por=ordenar_por,
            ordem=ordem
        )

    # ---------------------------------------------------------
    # CONSULTA SIMPLES
    # ---------------------------------------------------------
    def listar_todos(self):
        return self.repo.find()

    # ---------------------------------------------------------
    # BUSCAR POR ID
    # ---------------------------------------------------------
    def buscar_por_id(self, id: int):
        return self.repo.find_by_id(id)

    # ---------------------------------------------------------
    # REMOVER
    # ---------------------------------------------------------
    def remover(self, id: int):
        self.repo.delete(id)
        return True
