from ormar.exceptions import NoMatch
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from ..models.auth import TokenBearer, TokenData
from fastapi import Request, HTTPException, Depends
from ..db import UserDB,CourseDB
from ..models.user import User, UserRoles


load_dotenv()
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise Exception("JWT KEY NOT SUPPLIED")


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


async def check_user_course_privileged(course_code:str,user:User=Depends(get_current_user)):
    async def check_course():
        try:
            if user.role == UserRoles.admin:
                return user
            elif user.role == UserRoles.creator:
                course = await CourseDB.objects.get(course_code=course_code)
                # if course_code in courses:
                #     return user
            pass
        except Exception as e:
            if type(e) == NoMatch:
                raise HTTPException(detail="user not privileged to modify course",status_code=400)
            pass
    pass


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
