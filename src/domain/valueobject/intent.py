from typing import Literal


class Intent:
    def __init__(self, is_company_query: bool, type: Literal["company_query", "greeting", "out_of_scope", "unclear"]):
        self.is_company_query = is_company_query
        self.type = type

    def out_of_scope() -> Intent:
        return Intent(is_company_query=False, type="out_of_scope")
