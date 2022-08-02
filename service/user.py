
import hashlib
from service.auth import generate_password_hash
from dao.user import UserDAO
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_user_by_username(self, username):
        return self.dao.get_one_by_username(username)

    def get_all(self):
        return self.dao.get_all()

    def create(self, data):
        data["password"] = generate_password_hash(password=data["password"])
        return self.dao.create(data)

    def update(self, data):
        self.dao.update(data)
        return self.dao

    def delete(self, user_id):
        self.dao.delete(user_id)

    def get_hash(self, password):
        # Метод хеширования пароля
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

