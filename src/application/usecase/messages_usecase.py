from src.domain.port import MessageRepository, ChatRepository, UserRepository
from src.domain.valueobject import IdentityProviderId, PrimaryKey


class MessageUseCase:
    def __init__(self, message_repo: MessageRepository,
                 chat_repository: ChatRepository,
                 user_repository: UserRepository):
        self.message_repo = message_repo
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def execute(self, chat_id: int, identity_provider: str):

        user = self.user_repository.get_user(
            IdentityProviderId(identity_provider))

        if user is None:
            raise Exception("User not found")

        chat = self.chat_repository.get_chat(
            PrimaryKey.from_str(chat_id), user.id)

        if chat is None:
            raise Exception("Chat not found")
        return self.message_repo.get_messages_by_chat_id(chat_id)
