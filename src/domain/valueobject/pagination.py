class CursorPagination:
    def __init__(self, limit: int, cursor_id: str, cursor_created_at: str, has_more: bool = False, items: list = None):
        self.limit = limit
        self.has_more = has_more
        self.items = items
        self.cursor_id = cursor_id
        self.cursor_created_at = cursor_created_at
