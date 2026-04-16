import time

from ..valueobject import PrimaryKey


class Chat:
    def __init__(self, id: PrimaryKey, title: str, user_id: PrimaryKey, department_id: PrimaryKey = None, model_id: PrimaryKey = None, created_at: str = None, updated_at: str = None, deleted_at: str = None):

        self.title = title
        self.id = id
        self.user_id = user_id

        self.department_id = department_id
        self.model_id = model_id

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    @staticmethod
    def create(user_id: PrimaryKey, title: str, model_id: PrimaryKey, department_id: PrimaryKey = None):
        return Chat(id=PrimaryKey.new_id(),
                    title=title,
                    user_id=user_id,
                    model_id=model_id,
                    department_id=department_id,
                    created_at=time.time())

    @staticmethod
    def reconstitute(id: PrimaryKey, title: str, user_id: PrimaryKey, model_id: PrimaryKey, department_id: PrimaryKey = None, created_at: str = None, updated_at: str = None, deleted_at: str = None):
        chat = Chat(id=id,
                    title=title,
                    user_id=user_id,
                    model_id=model_id,
                    department_id=department_id,
                    created_at=created_at,
                    updated_at=updated_at,
                    deleted_at=deleted_at)
        return chat

    def to_dict(self):
        return {
            "id": self.id.get_id(),
            "title": self.title,
            # "user_id": self.user_id.get_id(),
            # "department_id": self.department_id.get_id() if self.department_id else None,
            # "model_id": self.model_id.get_id() if self.model_id else None,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
            # "deleted_at": self.deleted_at
        }
