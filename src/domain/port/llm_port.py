
from abc import ABC, abstractmethod


class LLMPort(ABC):
    @abstractmethod
    def generate_answer(self, prompt: str, context: list) -> str:
        pass
