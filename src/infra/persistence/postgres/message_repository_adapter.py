from sqlalchemy.orm import Session

from src.domain.port import MessageRepository
from src.domain.model import Message
from .entities import MessageEntity


class MessageRepositoryAdapter(MessageRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_message(self, message: Message) -> Message:
        entity = MessageEntity.from_domain(message)
        self.db_session.add(entity)
        self.db_session.commit()
        return entity.to_domain()

    def get_messages_by_chat_id(self, chat_id: int) -> list[Message]:
        entities = self.db_session.query(
            MessageEntity).filter_by(chat_id=chat_id).all()
        return [entity.to_domain() for entity in entities]
