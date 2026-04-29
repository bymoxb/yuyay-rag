
from abc import ABC, abstractmethod
from src.domain.valueobject import Answer, Intent


class LLMPort(ABC):
    @abstractmethod
    def generate_answer(self, prompt: str, context: list) -> Answer:
        pass
