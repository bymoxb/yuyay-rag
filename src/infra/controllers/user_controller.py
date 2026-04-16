from flask import jsonify
from flask.views import MethodView

from src.application.usecase import GetUserByIdUseCase
from src.infra.security import AuthUser


class UserController(MethodView):
    def __init__(self, get_user_by_id_usecase: GetUserByIdUseCase):
        self.get_user_by_id_usecase = get_user_by_id_usecase

    def get(self):
        user = self.get_user_by_id_usecase.execute(AuthUser.username())

        if user:
            return jsonify({'ok': True, 'data': user.to_dict()}), 200
        else:
            return jsonify({'ok': False, 'error': 'User not found'}), 404
