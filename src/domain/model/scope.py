
from src.domain.model.department import Department


class UserScope:
    def __init__(self, user_scope_id: str, user_id: str, department: Department, direction: str):
        self.user_scope_id = user_scope_id
        self.user_id = user_id
        self.department = department
        self.direction = direction
