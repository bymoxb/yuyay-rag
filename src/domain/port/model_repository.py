
from abc import ABC, abstractmethod

from ..model import Model


class ModelRepository(ABC):
    @abstractmethod
    def get_model_by_name(self, name: str) -> Model:
        pass

    @abstractmethod
    def get_default_model(self):
        pass
