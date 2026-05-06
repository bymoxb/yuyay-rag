import time
import os

from src.domain.model import Chat, Message, Model
from src.domain.valueobject import IdentityProviderId, PrimaryKey
from src.domain.port import ChatRepository, MessageRepository, UserRepository, ModelRepository, LLMPort, VectorRepository


class ChatUseCase:
    def __init__(self,
                 chat_repository: ChatRepository,
                 user_repository: UserRepository,
                 message_repository: MessageRepository,
                 model_repository: ModelRepository,
                 vector_repository: VectorRepository,
                 with_router: bool = False):
        self.chat_repository = chat_repository
        self.user_repository = user_repository
        self.message_repository = message_repository
        self.model_repository = model_repository
        self.vector_repository = vector_repository
        self.with_router = with_router

    def execute(self, identity_provider: str, message: str, chat_id: str = None, model_name: str = None, llm_service: LLMPort = None):

        user = self.user_repository.get_user(
            IdentityProviderId(identity_provider))

        if user is None:
            raise Exception("User not found")

        llm_model: Model = None

        if not model_name:
            llm_model = self.model_repository.get_default_model()
        else:
            llm_model = self.model_repository.get_model_by_name(model_name)

        if llm_model is None:
            raise Exception("Model not found")

        chat: Chat = None

        if chat_id is None:
            chat = Chat.create(
                user_id=user.id,
                title=f"Chat de {user.name}",
                model_id=llm_model.id,)

            self.chat_repository.create_chat(chat)
        else:
            chat = self.chat_repository.get_chat(PrimaryKey.from_str(chat_id))

        if chat is None:
            raise Exception("Chat not found")

        user_message = Message.create(
            chat_id=chat.id,
            user_id=user.id,
            content=message,
            role="user")

        self.message_repository.create_message(user_message)

        answer = None

        if self.with_router:
            intent = llm_service.determine_intent(message)

            if intent.is_company_query:
                context = self.vector_repository.search_relevant_context(
                    message)
                answer = llm_service.generate_answer(message, context)
            else:
                answer = llm_service.fallback_answer(message)

        else:
            context = self.vector_repository.search_relevant_context(message)
            answer = llm_service.generate_answer(message, context)

        if answer is None:
            raise Exception("LLM did not return an answer")

        response_message = Message.create(
            chat_id=chat.id,
            user_id=user.id,
            content=answer.content,
            latency=answer.latency,
            tokens_completion=answer.tokens_completion,
            tokens_prompt=answer.tokens_prompt,
            role="assistant")

        self.message_repository.create_message(response_message)

        # self.chat_repository.update_chat_timestamp(chat.id)

        return response_message

    def execute_stream(self, identity_provider: str, message: str, chat_id: str = None, model_name: str = None, llm_service: LLMPort = None):
        if not message or len(message.strip()) == 0:
            raise ValueError("Query vacía")

        if len(message) > 500:
            raise ValueError("Query demasiado larga")

        context = self.vector_repository.search_relevant_context(message)

        return llm_service.stream_answer(message, context)


class GetChatsUseCase:
    def __init__(self, chat_repository: ChatRepository, user_repository: UserRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def execute(self, identity_provider):
        user = self.user_repository.get_user(
            IdentityProviderId(identity_provider))

        if user is None:
            raise Exception("User not found")

        chats = self.chat_repository.get_chats(user.id)

        return chats
