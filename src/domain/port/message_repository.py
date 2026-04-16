

from abc import ABC, abstractmethod
from src.domain.model.message import Message


class MessageRepository(ABC):

    @abstractmethod
    def create_message(self, message: Message) -> Message:
        pass
