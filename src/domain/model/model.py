
from ..valueobject import PrimaryKey


class Model:
    def __init__(self, id: PrimaryKey, name: str, is_default: bool = False):
        self.id = id
        self.name = name
        self.is_default = is_default

    def reconstitute(id: PrimaryKey, name: str, is_default: bool = False) -> 'Model':
        return Model(id=id, name=name, is_default=is_default)

    def to_dict(self):
        return {
            "id": self.id.get_id(),
            "name": self.name,
            "is_default": self.is_default
        }
