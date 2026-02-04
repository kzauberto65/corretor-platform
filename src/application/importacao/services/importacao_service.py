from src.domain.importacao.dto.importacao_input_dto import ImportacaoInputDTO
from src.domain.importacao.dto.importacao_dto import ImportacaoDTO
from src.domain.importacao.entities.importacao_entity import ImportacaoEntity
from src.application.importacao.normalizers.importacao_normalizer import ImportacaoNormalizer
from src.infrastructure.importacao.repositories.importacao_repository import ImportacaoRepository

class ImportacaoService:

    def __init__(self, repository: ImportacaoRepository):
        self.repository = repository

    def cadastrar(self, dto: ImportacaoInputDTO) -> ImportacaoDTO:
        normalized = ImportacaoNormalizer.normalize(dto)
        entity = ImportacaoEntity(
            id=None,
            tipo=normalized.tipo,
            arquivo=normalized.arquivo,
            origem=normalized.origem,
            total_registros=normalized.total_registros,
            status=normalized.status,
            data_execucao=normalized.data_execucao,
            sucesso=normalized.sucesso,
            erros=normalized.erros,
            log=normalized.log
        )
        created = self.repository.cadastrar(entity)
        return ImportacaoDTO(**created.__dict__)

    def atualizar(self, id: int, dto: ImportacaoInputDTO) -> ImportacaoDTO:
        normalized = ImportacaoNormalizer.normalize(dto)
        entity = ImportacaoEntity(
            id=id,
            tipo=normalized.tipo,
            arquivo=normalized.arquivo,
            origem=normalized.origem,
            total_registros=normalized.total_registros,
            status=normalized.status,
            data_execucao=normalized.data_execucao,
            sucesso=normalized.sucesso,
            erros=normalized.erros,
            log=normalized.log
        )
        updated = self.repository.atualizar(entity)
        return ImportacaoDTO(**updated.__dict__)

    def consultar(self) -> list[ImportacaoDTO]:
        lista = self.repository.consultar()
        return [ImportacaoDTO(**item.__dict__) for item in lista]

    def buscar_por_id(self, id: int) -> ImportacaoDTO | None:
        encontrado = self.repository.buscar_por_id(id)
        return ImportacaoDTO(**encontrado.__dict__) if encontrado else None

    def remover(self, id: int) -> bool:
        return self.repository.remover(id)
