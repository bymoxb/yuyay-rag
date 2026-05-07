import os
import dotenv

from flask import Flask, Blueprint
from flask_cors import CORS
from llama_index.embeddings.ollama import OllamaEmbedding

from src.application.usecase import GetUserByIdUseCase, ChatUseCase, GetChatsUseCase
from src.infra.controllers import UserController, ChatController, ChatStreamController
from src.infra.persistence.postgres import db, UserRepositoryAdapter, ChatRepositoryAdapter, MessageRepositoryAdapter, ModelRepositoryAdapter
from src.infra.security import Oauth
from src.infra.persistence.chroma import ChromaVectorRepositoryAdapter


def create_app():

    if os.getenv('ENV') != 'production':
        dotenv.load_dotenv()

    app = Flask(__name__)

    # 0. Configuración de Seguridad
    app.config["JWKS_URL"] = os.getenv("JWKS_URL")
    app.config["JWT_ISSUER"] = os.getenv("JWT_ISSUER")
    app.config["JWT_CLIENT_ID"] = os.getenv("JWT_CLIENT_ID")

    Oauth(app)

    # 1. Inicializar DB
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)

    # 2. Inyección de Dependencias Manual
    embed_model = OllamaEmbedding(model_name=os.getenv("EMBED_MODEL"))
    chromadb = ChromaVectorRepositoryAdapter(
        host=os.getenv("CROMA_HOST"),
        port=int(os.getenv("CROMA_PORT")),
        collection_name=os.getenv("CROMA_COLLECTION"),
        embed_model=embed_model,
        similarity_top_k=int(os.getenv("SIMILARITY_TOP_K", 5))
    )

    chat_repo = ChatRepositoryAdapter(db.session)
    message_repo = MessageRepositoryAdapter(db.session)
    user_repo = UserRepositoryAdapter(db.session)
    model_repo = ModelRepositoryAdapter(db.session)

    chat_usecase = ChatUseCase(
        chat_repo,
        user_repo,
        message_repo,
        model_repo,
        vector_repository=chromadb,
        with_router=os.getenv("WITH_ROUTER", "False").lower() == "true")
    get_user_by_id_usecase = GetUserByIdUseCase(user_repo)
    get_chats_usecase = GetChatsUseCase(chat_repo, user_repo)

    # 3. Configurar Blueprints y Rutas
    user_bp = Blueprint('user_bp', __name__)
    chat_bp = Blueprint('chat_bp', __name__)
    chat_stream_bp = Blueprint('chat_stream_bp', __name__)

    # Convertimos la clase en una "vista" de Flask inyectando el servicio
    user_view = UserController.as_view(
        'user_api', get_user_by_id_usecase=get_user_by_id_usecase)
    chat_view = ChatController.as_view(
        'chat_api', chat_usecase=chat_usecase, get_chats_usecase=get_chats_usecase)
    chat_stream_view = ChatStreamController.as_view(
        'chat_stream_api', chat_usecase=chat_usecase)

    # Definir reglas de rutas
    user_bp.add_url_rule('/user', view_func=user_view, methods=['GET', 'POST'])
    user_bp.add_url_rule('/user/<string:user_id>',
                         view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

    chat_bp.add_url_rule('/chat', view_func=chat_view, methods=['GET', 'POST'])
    chat_bp.add_url_rule('/chat', view_func=chat_view, methods=['POST'])
    chat_stream_bp.add_url_rule(
        '/stream', view_func=chat_stream_view, methods=['POST'])

    # 4. Registrar Blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(chat_stream_bp, url_prefix='/api')

    # 5. Configuracion de cors
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
