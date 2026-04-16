from abc import ABC, abstractmethod

from ..model import Chat
from ..valueobject import IdentityProviderId, PrimaryKey


class ChatRepository(ABC):

    @abstractmethod
    def get_chat(self, chat_id: PrimaryKey) -> Chat:
        pass

    @abstractmethod
    def create_chat(self, chat: Chat):
        pass

    @abstractmethod
    def get_chats(self, user_id: PrimaryKey) -> list[Chat]:
        pass
