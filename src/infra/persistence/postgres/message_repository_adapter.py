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
