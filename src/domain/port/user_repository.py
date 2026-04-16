from abc import ABC, abstractmethod

from ..valueobject import IdentityProviderId
from ..model import User


class UserRepository(ABC):

    @abstractmethod
    def get_user(self, identity_provider: IdentityProviderId) -> User:
        pass
