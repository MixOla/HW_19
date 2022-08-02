from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def post(self):
        data = request.json
        return UserSchema().dump(user_service.create(data)), 201

#     def put(self, bid):
#         req_json = request.json
#         if "id" not in req_json:
#             req_json["id"] = bid
#         user_service.update(req_json)
#         return "", 204
#
#     def delete(self, bid):
#         user_service.delete(bid)
#         return "", 204
