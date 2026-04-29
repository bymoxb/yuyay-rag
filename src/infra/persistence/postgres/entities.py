
from src.infra.persistence.postgres import db
from src.domain.model import User, Model, Chat, Message
from src.domain.valueobject import PrimaryKey


class UserEntity(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)

    def to_domain(self) -> User:
        return User.reconstitute(
            id=PrimaryKey(self.id),
            name=self.full_name,
            email=self.email,
            user_scopes=[]
        )


class ModelEntity(db.Model):
    __tablename__ = 'model'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)
    is_default = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_domain(self):
        return Model.reconstitute(
            id=PrimaryKey(self.id),
            name=self.name,
            is_default=self.is_default
        )


class DepartmentEntity(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.String(36), primary_key=True)
    code = db.Column(db.String(32), nullable=False, unique=True)
    name = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)


class ChatEntity(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'user.id'), nullable=False)
    department_id = db.Column(
        db.String(36), db.ForeignKey('department.id'), nullable=True)
    model_id = db.Column(
        db.String(36), db.ForeignKey('model.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_domain(self):
        return Chat.reconstitute(
            id=PrimaryKey(self.id),
            title=self.title,
            user_id=PrimaryKey(self.user_id),
            department_id=PrimaryKey(
                self.department_id) if self.department_id else None,
            model_id=PrimaryKey(self.model_id) if self.model_id else None,
            created_at=self.created_at.timestamp() if self.created_at else None,
            updated_at=self.updated_at.timestamp() if self.updated_at else None,
            deleted_at=self.deleted_at.timestamp() if self.deleted_at else None
        )

    def from_domain(chat: Chat) -> 'ChatEntity':
        entity = ChatEntity(
            id=chat.id.get_id(),
            title=chat.title,
            user_id=chat.user_id.get_id(),
            # department_id=chat.department_id.get_id() if chat.department_id else None,
            model_id=chat.model_id.get_id() if chat.model_id else None,
            created_at=db.func.now()
        )

        return entity

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id,
            "department_id": self.department_id,
            "model_id": self.model_id,
            # "created_at": self.created_at.isoformat() if self.created_at is else None,
            # "updated_at": self.updated_at.isoformat() if self.updated_at is else None,
            # "deleted_at": self.deleted_at.isoformat() if self.deleted_at is else None
        }


class MessageEntity(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.String(36), primary_key=True)
    chat_id = db.Column(db.String(36), db.ForeignKey(
        'chat.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey(
        'user.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)  # user, assistant, system

    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def to_domain(self):
        return Message.reconstitute(
            id=PrimaryKey(self.id),
            chat_id=PrimaryKey(self.chat_id),
            content=self.content,
            user_id=PrimaryKey(self.user_id) if self.user_id else None,
            role=self.role,
            created_at=self.created_at.timestamp() if self.created_at else None,
            # updated_at=self.updated_at.timestamp() if self.updated_at else None,
            # deleted_at=self.deleted_at.timestamp() if self.deleted_at else None
        )

    def from_domain(message: Message) -> 'MessageEntity':
        entity = MessageEntity(
            id=message.id.get_id(),
            chat_id=message.chat_id.get_id(),
            user_id=message.user_id.get_id(),
            content=message.content,
            role=message.role,
            created_at=db.func.now()
        )

        return entity
