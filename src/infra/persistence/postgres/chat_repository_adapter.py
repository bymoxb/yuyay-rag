from sqlalchemy.orm import Session

from src.domain.model import Chat
from src.domain.port import ChatRepository
from src.domain.valueobject import IdentityProviderId, PrimaryKey
from .entities import ChatEntity


class ChatRepositoryAdapter(ChatRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_chat(self, chat: Chat):
        chat_entity = ChatEntity.from_domain(chat)
        print(chat_entity.to_dict())
        self.db_session.add(chat_entity)
        self.db_session.commit()
        return chat_entity.to_domain()

    def get_chat(self, chat_id: PrimaryKey):
        chat_entity = self.db_session.query(ChatEntity).filter(
            ChatEntity.id == chat_id.get_id()).first()

        return chat_entity.to_domain() if chat_entity else None

    def get_chats(self, user_id: PrimaryKey):
        chat_entities = self.db_session.query(ChatEntity).filter(
            ChatEntity.user_id == user_id.get_id()).order_by(ChatEntity.created_at.desc()).all()

        return [chat_entity.to_domain() for chat_entity in chat_entities] if chat_entities else []
