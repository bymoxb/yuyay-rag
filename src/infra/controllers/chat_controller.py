from flask import jsonify, request
from flask.views import MethodView

from src.application.usecase import ChatUseCase, GetChatsUseCase
from src.infra.security import AuthUser


class ChatController(MethodView):

    def __init__(self, chat_usecase: ChatUseCase, get_chats_usecase: GetChatsUseCase):
        self.chat_usecase = chat_usecase
        self.get_chats_usecase = get_chats_usecase

    def get(self):
        chats = self.get_chats_usecase.execute(
            AuthUser.username())
        chats_data = [chat.to_dict() for chat in chats]
        return jsonify({"ok": True, "data": chats_data}), 200

    def post(self):
        data = request.get_json()
        # print("data", data)
        message = self.chat_usecase.execute(
            message=data.get("message"),
            identity_provider=AuthUser.username(),
            chat_id=data.get("chat_id"),
            model_name=data.get("model"),
        )

        return jsonify({"ok": True, "data": message}), 200
