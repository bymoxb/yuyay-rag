from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from src.domain.model import Chat
from src.domain.port import ChatRepository
from src.domain.valueobject import IdentityProviderId, PrimaryKey, CursorPagination
from .entities import ChatEntity


class ChatRepositoryAdapter(ChatRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_chat(self, chat: Chat):
        chat_entity = ChatEntity.from_domain(chat)
        self.db_session.add(chat_entity)
        self.db_session.commit()
        return chat_entity.to_domain()

    def get_chat(self, chat_id: PrimaryKey, user_id: PrimaryKey):
        chat_entity = self.db_session.query(ChatEntity).filter(
            ChatEntity.id == chat_id.get_id(),
            ChatEntity.user_id == user_id.get_id()
        ).first()

        return chat_entity.to_domain() if chat_entity else None

    def get_chats(self, limit: int, user_id: PrimaryKey, cursor_id: PrimaryKey = None, cursor_created_at: str = None) -> CursorPagination:

        query = (
            self.db_session.query(ChatEntity)
            .filter(
                ChatEntity.user_id == user_id.get_id(),
                ChatEntity.deleted_at.is_(None)
            )
        )

        # Cursor pagination
        if cursor_created_at and cursor_id:
            query = query.filter(
                or_(
                    ChatEntity.created_at < cursor_created_at,

                    and_(
                        ChatEntity.created_at == cursor_created_at,
                        ChatEntity.id < cursor_id
                    )
                )
            )

        # Orden estable
        query = query.order_by(
            desc(ChatEntity.created_at),
            desc(ChatEntity.id)
        )

        # Pedimos uno extra para detectar has_more
        rows = query.limit(limit + 1).all()

        has_more = len(rows) > limit

        # Dejamos sólo el límite real
        rows = rows[:limit]

        chats = [row.to_domain() for row in rows]

        next_cursor_created_at = None
        next_cursor_id = None

        # Generar siguiente cursor
        if has_more and rows:
            last_row = rows[-1]

            next_cursor_created_at = last_row.created_at.isoformat()
            next_cursor_id = str(last_row.id)

        return CursorPagination(
            items=chats,
            limit=limit,
            cursor_id=next_cursor_id,
            cursor_created_at=next_cursor_created_at,
            has_more=has_more,
        )
