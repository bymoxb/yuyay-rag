
from ..valueobject import PrimaryKey
from .role import Role
from .scope import UserScope


class User:
    def __init__(self, id: PrimaryKey, name: str, email: str, roles: list[Role] = None, user_scopes: list[UserScope] = None):
        self.id = id
        self.name = name
        self.email = email
        self.roles = roles or []
        self.user_scopes = user_scopes or []

    @staticmethod
    def reconstitute(id: PrimaryKey, name: str, email: str, roles: list[Role] = None, user_scopes: list[UserScope] = None):
        return User(id=id, name=name, email=email, roles=roles, user_scopes=user_scopes)

    def has_permission(self, code: str) -> bool:
        for role in self.roles:
            for functionality in role.functionalities:
                if functionality.code == code:
                    return True
        return False

    def get_scope_codes(self) -> list[str]:
        return [scope.department.code for scope in self.user_scopes]

    def to_dict(self):
        return {
            'id': self.id.get_id(),
            'fullName': self.name,
            'email': self.email,
            'roles': [role.name for role in self.roles],
            'functionalities': [func.code for role in self.roles for func in role.functionalities],
        }
