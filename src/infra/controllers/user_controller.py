from flask import jsonify, Blueprint
from src.infra.security import AuthUser


def UserController(get_user_by_id_usecase):
    users_bp = Blueprint("user_api", __name__)

    @users_bp.get("/users")
    def get():
        user = get_user_by_id_usecase.execute(AuthUser.username())

        if user:
            return jsonify({'ok': True, 'data': user.to_dict()}), 200
        else:
            return jsonify({'ok': False, 'error': 'User not found'}), 404

    return users_bp
