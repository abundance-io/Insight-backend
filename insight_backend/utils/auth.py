from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from ..models.auth import JwtBearer

load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


def hash_password(unhashed: str) -> str:
    return bcrypt.hash(unhashed)


def verify_hash(unhashed: str, hash: str) -> bool:
    return bcrypt.verify(unhashed, hash)


def create_access_token(telegram_id: str) -> JwtBearer:
    # set to expire in 1 day
    to_encode = {
        "telegram_id": telegram_id,
        "exp": datetime.utcnow() + timedelta(minutes=1440),
    }

    token = jwt.encode(to_encode, JWT_SECRET_KEY)

    return JwtBearer(**{"token": token})


def get_current_user():
    pass
