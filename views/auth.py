
from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import user_service
from service.auth import generate_tokens, approve_token

auth_ns = Namespace('auth')

@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        """ Авторизация пользователя """
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)

        if not username or not password:
            return "Нет пароля или логина", 400

        user = user_service.get_user_by_username(username=username)

        return generate_tokens(username=username,
                               password=password,
                               password_hash=user.password,
                               is_refresh=False), 201



    def put(self):
        data = request.json
        if not data.get("refresh_token"):
            return "", 400

        return approve_token(data.get("refresh_token")), 200

