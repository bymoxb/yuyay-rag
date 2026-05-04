from flask import jsonify, request
from flask.views import MethodView

from src.application.usecase import ChatUseCase, GetChatsUseCase
from src.infra.security import AuthUser
from src.infra.factories.llm_factory import LLMFactory
from src.infra.security.oauth import has_role


class ChatController(MethodView):

    def __init__(self, chat_usecase: ChatUseCase, get_chats_usecase: GetChatsUseCase):
        self.chat_usecase = chat_usecase
        self.get_chats_usecase = get_chats_usecase

    @has_role(['role_user'])
    def get(self):
        chats = self.get_chats_usecase.execute(
            AuthUser.username())
        chats_data = [chat.to_dict() for chat in chats]
        return jsonify({"ok": True, "data": chats_data}), 200

    @has_role(['role_user'])
    def post(self):
        data = request.get_json()

        llm_service = LLMFactory.get_llm(model_name=data.get("model"))

        message = self.chat_usecase.execute(
            message=data.get("message"),
            identity_provider=AuthUser.username(),
            chat_id=data.get("chat_id"),
            model_name=data.get("model"),
            llm_service=llm_service
        )

        return jsonify({"ok": True, "data": message.to_dict()}), 200
