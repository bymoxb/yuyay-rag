

from abc import ABC, abstractmethod
from src.domain.model.message import Message


class MessageRepository(ABC):

    @abstractmethod
    def create_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    def get_messages_by_chat_id(self, chat_id: int) -> list['Message']:
        pass
