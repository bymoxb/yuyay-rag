
import time

from ..valueobject import PrimaryKey


class Message:
    def __init__(self, id: PrimaryKey, chat_id: PrimaryKey, role: str, content: str, user_id: PrimaryKey, created_at: str):
        self.id = id
        self.chat_id = chat_id
        self.role = role
        self.content = content
        self.user_id = user_id
        self.created_at = created_at

    @staticmethod
    def create(chat_id: PrimaryKey, user_id: PrimaryKey, content: str, role: str):
        return Message(id=PrimaryKey.new_id(),
                       chat_id=chat_id,
                       role=role,
                       content=content,
                       user_id=user_id,
                       created_at=time.time())

    @staticmethod
    def reconstitute(id: PrimaryKey, chat_id: PrimaryKey, role: str, content: str, user_id: PrimaryKey, created_at: str):
        return Message(id=id,
                       chat_id=chat_id,
                       role=role,
                       content=content,
                       user_id=user_id,
                       created_at=created_at)
