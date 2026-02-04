from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.empreendimento.dto.empreendimento_dto import EmpreendimentoDTO
from src.domain.empreendimento.dto.empreendimento_filter_dto import EmpreendimentoFilterDTO


class IEmpreendimentoRepository(ABC):
    """
    Interface de repositório para operações de persistência
    relacionadas ao domínio Empreendimento.
    """

    @abstractmethod
    def save(self, dto: EmpreendimentoDTO) -> EmpreendimentoDTO:
        """
        Insere um novo empreendimento no banco.
        Retorna o DTO já com o ID preenchido.
        """
        pass

    @abstractmethod
    def update(self, dto: EmpreendimentoDTO) -> EmpreendimentoDTO:
        """
        Atualiza um empreendimento existente.
        """
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Remove um empreendimento pelo ID.
        """
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[EmpreendimentoDTO]:
        """
        Busca um empreendimento pelo ID.
        """
        pass

    @abstractmethod
    def find(self, filtro: EmpreendimentoFilterDTO) -> List[EmpreendimentoDTO]:
        """
        Busca empreendimentos usando filtros opcionais.
        """
        pass
