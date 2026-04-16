
from src.domain.model import User
from src.domain.port import UserRepository
from src.domain.valueobject import IdentityProviderId


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id) -> User:
        return self.user_repository.get_user(IdentityProviderId(user_id))
