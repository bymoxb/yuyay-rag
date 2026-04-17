
from abc import ABC, abstractmethod


class VectorRepository(ABC):
    @abstractmethod
    def search_relevant_context(self, query: str) -> list:
        """Busca texto relevante basado en una consulta."""
        pass
