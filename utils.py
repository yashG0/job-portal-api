from typing import Any
from datetime import datetime
from os import getenv

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

JWT_KEY = getenv("JWT_SECRET")
ph = PasswordHasher()


if JWT_KEY is None:
    raise ValueError("SECRET_KEY not found")


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False


def create_access_token(payload: dict[str, Any]) -> str:
    return jwt.encode(payload, key=JWT_KEY, algorithm="HS256")


def decode_access_token(encoded_jwt) -> dict[str, Any]:
    return jwt.decode(encoded_jwt, key=JWT_KEY, algorithms=["HS256"])
