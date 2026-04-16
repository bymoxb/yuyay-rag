
from ..valueobject import PrimaryKey


class Functionality:
    def __init__(self, id: PrimaryKey, code: str, name: str):
        self.id = id
        self.code = code
        self.name = name

    def reconstitute(self, id: PrimaryKey, code: str, name: str) -> 'Functionality':
        return Functionality(id=id, code=code, name=name)
