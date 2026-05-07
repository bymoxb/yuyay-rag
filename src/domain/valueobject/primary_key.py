import uuid


class PrimaryKey:
    def __init__(self, id: str):
        self.id = id

    @staticmethod
    def new_id():
        return PrimaryKey(id=str(uuid.uuid4()))

    @staticmethod
    def from_str(id_str: str):
        return PrimaryKey(id=str(uuid.UUID(id_str)))

    def get_id(self) -> str:
        return self.id

    def to_str(self) -> str:
        return str(self.id)
