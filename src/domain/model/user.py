
from ..valueobject import PrimaryKey
# from .role import Role
from .scope import UserScope


class User:
    def __init__(self, id: PrimaryKey, name: str, email: str, user_scopes: list[UserScope] = None):
        self.id = id
        self.name = name
        self.email = email
        self.user_scopes = user_scopes or []

    @staticmethod
    def reconstitute(id: PrimaryKey, name: str, email: str, user_scopes: list[UserScope] = None):
        return User(id=id, name=name, email=email, user_scopes=user_scopes)

    def get_scope_codes(self) -> list[str]:
        return [scope.department.code for scope in self.user_scopes]

    def to_dict(self):
        return {
            'id': self.id.get_id(),
            'fullName': self.name,
            'email': self.email,
        }
