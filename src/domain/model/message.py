
import time

from ..valueobject import PrimaryKey


class Message:
    def __init__(self, id: PrimaryKey, chat_id: PrimaryKey, role: str, content: str, user_id: PrimaryKey, latency: int, tokens_prompt: int, tokens_completion: int, retrieval_context: dict, rating: int, created_at: str):
        self.id = id
        self.chat_id = chat_id
        self.role = role
        self.content = content
        self.user_id = user_id
        self.latency = latency
        self.tokens_prompt = tokens_prompt
        self.tokens_completion = tokens_completion
        self.retrieval_context = retrieval_context
        self.rating = rating
        self.created_at = created_at

    @staticmethod
    def create(chat_id: PrimaryKey, user_id: PrimaryKey, content: str, role: str, latency: int = 0, tokens_prompt: int = 0, tokens_completion: int = 0, retrieval_context: dict = None):
        return Message(id=PrimaryKey.new_id(),
                       chat_id=chat_id,
                       role=role,
                       content=content,
                       user_id=user_id,
                       latency=latency,
                       tokens_prompt=tokens_prompt,
                       tokens_completion=tokens_completion,
                       retrieval_context=retrieval_context,
                       rating=None,
                       created_at=time.time())

    @staticmethod
    def reconstitute(id: PrimaryKey, chat_id: PrimaryKey, role: str, content: str, user_id: PrimaryKey, latency: int, tokens_prompt: int, tokens_completion: int, retrieval_context: dict, rating: int, created_at: str):
        return Message(id=id,
                       chat_id=chat_id,
                       role=role,
                       content=content,
                       user_id=user_id,
                       latency=latency,
                       tokens_prompt=tokens_prompt,
                       tokens_completion=tokens_completion,
                       retrieval_context=retrieval_context,
                       rating=rating,
                       created_at=created_at)

    def to_dict(self):
        return {
            "id": self.id.get_id(),
            "chat_id": self.chat_id.get_id(),
            "role": self.role,
            "content": self.content,
            "user_id": self.user_id.get_id(),
            "created_at": self.created_at,
            "latency": self.latency,
            "tokens_prompt": self.tokens_prompt,
            "tokens_completion": self.tokens_completion,
            "retrieval_context": self.retrieval_context,
            "rating": self.rating,
        }
