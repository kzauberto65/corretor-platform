from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.lead.entities.lead_entity import LeadEntity


class LeadRepository(ABC):
    """
    Interface do repositório de Lead.
    Segue o mesmo padrão do MailingRepository.
    """

    # -------------------------
    # CRUD básico
    # -------------------------
    @abstractmethod
    def create(self, entity: LeadEntity) -> int:
        """Cria um novo lead e retorna o ID gerado."""
        pass

    @abstractmethod
    def update(self, entity: LeadEntity) -> None:
        """Atualiza um lead existente."""
        pass

    @abstractmethod
    def delete(self, lead_id: int) -> None:
        """Remove um lead pelo ID."""
        pass

    @abstractmethod
    def get_by_id(self, lead_id: int) -> Optional[LeadEntity]:
        """Retorna um lead pelo ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[LeadEntity]:
        """Lista todos os leads."""
        pass

    # -------------------------
    # Filtros
    # -------------------------
    @abstractmethod
    def filter_by_status(self, status: str) -> List[LeadEntity]:
        pass

    @abstractmethod
    def filter_by_intencao(self, intencao: str) -> List[LeadEntity]:
        pass

    @abstractmethod
    def filter_by_faixa_preco(self, preco_min: float, preco_max: float) -> List[LeadEntity]:
        pass

    @abstractmethod
    def filter_by_cidade(self, cidade: str) -> List[LeadEntity]:
        pass

    @abstractmethod
    def filter_by_bairro(self, bairro: str) -> List[LeadEntity]:
        pass

    @abstractmethod
    def filter_by_urgencia(self, urgencia: str) -> List[LeadEntity]:
        pass

    # -------------------------
    # Histórico
    # -------------------------
    @abstractmethod
    def append_historico(self, lead_id: int, evento: dict) -> None:
        """Adiciona um evento ao histórico do lead."""
        pass

    # -------------------------
    # Score
    # -------------------------
    @abstractmethod
    def update_score(self, lead_id: int, score: float) -> None:
        """Atualiza o score do lead."""
        pass
