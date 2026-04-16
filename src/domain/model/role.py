
from .functionality import Functionality
from ..valueobject import PrimaryKey


class Role:
    def __init__(self, id: PrimaryKey, name: str, functionalities: list[Functionality]):
        self.id = id
        self.name = name
        self.functionalities = functionalities

    def reconstitute(self, id: PrimaryKey, name: str, functionalities: list[Functionality] = []) -> 'Role':
        return Role(id=id, name=name, functionalities=functionalities)
