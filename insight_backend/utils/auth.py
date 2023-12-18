from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from ..models.auth import TokenBearer, TokenData
from fastapi import Request, HTTPException, Depends
from ..db import UserDB
from ..models.user import User, UserRoles


load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")


def hash_password(unhashed: str) -> str:
    return bcrypt.hash(unhashed)


def verify_hash(unhashed: str, hash: str) -> bool:
    return bcrypt.verify(unhashed, hash)


async def get_current_user(request: Request) -> User:
    token = request.headers.get("passkey")
    if token:
        try:
            data = jwt.decode(token, JWT_SECRET_KEY)
            telegram_id = data["telegram_id"]
            user = await UserDB.objects.get(telegram_id=telegram_id)
            return User(**user.dict())

        # todo better error coverage
        except Exception as e:
            raise HTTPException(detail="invalid passkey", status_code=401)
    else:
        raise HTTPException(detail="no passkey", status_code=400)


def check_current_user_admin(user: User = Depends(get_current_user)) -> User:
    if user.role == UserRoles.admin:
        return user
    else:
        raise HTTPException(detail="user is not an admin", status_code=401)


def create_access_token(telegram_id: str) -> TokenBearer:
    # set to expire in 1 day
    to_encode = {
        "telegram_id": telegram_id,
        "exp": datetime.utcnow() + timedelta(minutes=1440),
    }

    token = jwt.encode(to_encode, JWT_SECRET_KEY)

    return TokenBearer(**{"token": token})
