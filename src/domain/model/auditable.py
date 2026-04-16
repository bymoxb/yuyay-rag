
import time


class Auditable():
    def __init__(self, updated_at: str = None, deleted_at: str = None):
        self.created_at = time.time()
        self.updated_at = None
        self.deleted_at = None
