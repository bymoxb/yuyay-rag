
from src.domain.model import Chat, Message, Model
from src.domain.valueobject import IdentityProviderId, PrimaryKey
from src.domain.port import ChatRepository, MessageRepository, UserRepository, ModelRepository


class ChatUseCase:
    def __init__(self,
                 chat_repository: ChatRepository,
                 user_repository: UserRepository,
                 message_repository: MessageRepository,
                 model_repository: ModelRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository
        self.message_repository = message_repository
        self.model_repository = model_repository

    def execute(self, identity_provider, message, chat_id=None, model_name=None):

        user = self.user_repository.get_user(
            IdentityProviderId(identity_provider))

        if user is None:
            raise Exception("User not found")

        if user.has_permission("chat") is False:
            raise Exception("User does not have permission to chat")

        llm_model: Model = None

        if not model_name:
            llm_model = self.model_repository.get_default_model()
        else:
            llm_model = self.model_repository.get_model_by_name(model_name)

        if llm_model is None:
            raise Exception("Model not found")

        print("Model seleccionado:", llm_model.to_dict())

        chat: Chat = None

        if chat_id is None:
            chat = Chat.create(
                user_id=user.id,
                title=f"Chat de {user.name}",
                model_id=llm_model.id,)

            self.chat_repository.create_chat(chat)
        else:
            chat = self.chat_repository.get_chat(PrimaryKey.from_str(chat_id))

        user_message = Message.create(
            chat_id=chat.id,
            user_id=user.id,
            content=message,
            role="user")

        # 1. Obtener el modelo con el que se va a generar la respuesta
        # 2. Con el modelo, generar la respuesta a partir del mensaje del usuario
        # 3. Guardar el mensaje del usuario y la respuesta generada en la base de datos

        self.message_repository.create_message(user_message)
        # self.message_repository.create_message(response_message)

        # self.chat_repository.update_chat_timestamp(chat.id)

        # return response_message


class GetChatsUseCase:
    def __init__(self, chat_repository: ChatRepository, user_repository: UserRepository):
        self.chat_repository = chat_repository
        self.user_repository = user_repository

    def execute(self, identity_provider):
        user = self.user_repository.get_user(
            IdentityProviderId(identity_provider))

        if user is None:
            raise Exception("User not found")

        if user.has_permission("chat") is False:
            raise Exception("User does not have permission to chat")

        chats = self.chat_repository.get_chats(user.id)

        return chats
