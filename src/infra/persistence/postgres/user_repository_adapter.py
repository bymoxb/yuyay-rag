from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session

from src.domain.valueobject import IdentityProviderId
from src.domain.port import UserRepository
from src.domain.model import User
from src.infra.persistence.postgres import db, RoleEntity, UserEntity


class UserRepositoryAdapter(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, identity_provider: IdentityProviderId) -> User:
        user_entity = self.session.query(UserEntity)\
            .options(joinedload(UserEntity.roles).joinedload(RoleEntity.functionalities))\
            .filter(UserEntity.email == identity_provider.get_id())\
            .first()

        if not user_entity:
            return None

        # print("Repository ==========================")
        # for role in user_entity.roles:
        #     print(f"Role: {role.name}")
        #     for func in role.functionalities:
        #         print(f"  Functionality: {func.name}")

        return user_entity.to_domain(roles=user_entity.roles) if user_entity else None
