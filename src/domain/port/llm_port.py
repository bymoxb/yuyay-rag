
from abc import ABC, abstractmethod
from src.domain.valueobject import Answer, Intent


class LLMPort(ABC):

    @abstractmethod
    def determine_intent(self, query: str) -> Intent:
        pass

    @abstractmethod
    def fallback_answer(self, query: str) -> object:
        pass

    @abstractmethod
    def generate_answer(self, prompt: str, context: list) -> Answer:
        pass
