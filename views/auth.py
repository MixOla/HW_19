
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
        role = req_json.get("role", None)
        if not username or not password:
            return "Нет пароля или логина", 400

        password_hash = user_service.get_user_by_username(username=username).password
        return generate_tokens(username=username,
                               password=password,
                               password_hash=password_hash,
                               role=role,
                               is_refresh=False), 201



    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        return approve_token(req_json.get("refresh_token")), 200

