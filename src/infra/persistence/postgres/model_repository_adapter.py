from sqlalchemy.orm import Session

from src.domain.port import ModelRepository
from .entities import ModelEntity


class ModelRepositoryAdapter(ModelRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_model_by_name(self, name: str):
        model_entity = self.session.query(ModelEntity).filter(
            ModelEntity.name == name).first()

        return model_entity.to_domain() if model_entity else None

    def get_default_model(self):
        model_entity = self.session.query(ModelEntity).filter(
            ModelEntity.is_default == True).first()

        return model_entity.to_domain() if model_entity else None
