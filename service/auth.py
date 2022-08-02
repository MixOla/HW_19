import base64
import calendar
import datetime
import hashlib

from flask_restx import abort

from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


import jwt
from dao.helpers.decorators import secret, algo


def __generate_password(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    )


def generate_password_hash(password: str) -> str:
    return base64.b64encode(__generate_password(password)).decode('utf-8')


def compare_passwords_hash(password_hash, other_password) -> bool:
    return password_hash == generate_password_hash(other_password)


def generate_tokens(username, password_hash, password, role, is_refresh=False):

    if username is None:
        raise abort(404)

    if not is_refresh:
        if not compare_passwords_hash(password_hash=password_hash, other_password=password):
            return False

    data = {
        "username": username,
        "password": password,
        "role": role
    }

    # access token on 30 min
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)

    # refresh, 130 days
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algorithm=algo)
    tokens = {"access_token": access_token, "refresh_token": refresh_token}

    return tokens, 201


def approve_token(token):
    data = jwt.decode(token, key=secret, algorithm=algo)
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    return generate_tokens(username=username, password=password, role=role, is_refresh=True)
