import json

from flask import jsonify, request, Response, stream_with_context, Blueprint

from src.application.usecase import ChatUseCase, GetChatsUseCase, MessageUseCase
from src.infra.security import AuthUser
from src.infra.factories.llm_factory import LLMFactory
from src.infra.security.oauth import has_role


def ChatController(chat_usecase: ChatUseCase, get_chats_usecase: GetChatsUseCase, message_usecase: MessageUseCase):
    chat_bp = Blueprint('chat_bp', __name__)

    @has_role(['role_user'])
    @chat_bp.get('/chat')
    def get_chat():
        result = get_chats_usecase.execute(
            identity_provider=AuthUser.username(),
            limit=request.args.get("limit", default=10, type=int),
            cursor_id=request.args.get("cursor_id"),
            cursor_created_at=request.args.get("cursor_created_at")
        )
        chats = [chat.to_dict() for chat in result.items]
        return jsonify({
            "ok": True,
            "data": {
                "items": chats,
                "next_cursor_id": result.cursor_id,
                "next_cursor_created_at": result.cursor_created_at,
                "has_more": result.has_more,
            }}), 200

    @has_role(['role_user'])
    @chat_bp.post('/chat')
    def post_chat():
        data = request.get_json()

        llm_service = LLMFactory.get_llm(model_name=data.get("model"))

        message = chat_usecase.execute(
            message=data.get("message"),
            identity_provider=AuthUser.username(),
            chat_id=data.get("chat_id"),
            model_name=data.get("model"),
            llm_service=llm_service
        )

        return jsonify({"ok": True, "data": message.to_dict()}), 200

    @has_role(['role_user'])
    @chat_bp.post('/chat/stream')
    def post_stream():
        data = request.get_json()

        llm_service = LLMFactory.get_llm(model_name=data.get("model"))

        try:
            generator = chat_usecase.execute_stream(
                message=data.get("message"),
                identity_provider=AuthUser.username(),
                chat_id=data.get("chat_id"),
                model_name=data.get("model"),
                llm_service=llm_service
            )
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

        def generate():
            for event in generator:
                yield f"data: {json.dumps(event)}\n\n"

        return Response(
            stream_with_context(generate()),
            content_type="text/event-stream"
        )

    @has_role(['role_user'])
    @chat_bp.post('chat/<string:chat_id>/messages')
    def get_chat_history(chat_id):
        try:
            messages = message_usecase.execute(
                chat_id=chat_id,
                identity_provider=AuthUser.username()
            )
            messages_data = [msg.to_dict() for msg in messages]
            return jsonify({"ok": True, "data": messages_data}), 200
        except Exception as e:
            return jsonify({"ok": False, "error": str(e)}), 400

    return chat_bp
