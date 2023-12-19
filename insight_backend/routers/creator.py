from fastapi import APIRouter
from ..models.user import UserCred, User, UserRoles
from ..db import UserDB
from asyncpg.exceptions import UniqueViolationError
from ormar.exceptions import NoMatch
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from ..models.auth import TokenData

from ..utils.auth import (
    get_current_user,
    hash_password,
    verify_hash,
    create_access_token,
    check_current_user_admin,
)

creator_router = APIRouter()
router = creator_router


@router.post("/creator/")
async def authentiticate_creator(credentials: UserCred):
    try:
        user = await UserDB.objects.get(telegram_id=credentials.telegram_id)
    except NoMatch:
        raise HTTPException(detail="user does not exist", status_code=401)
    user = User(**user.dict())
    if verify_hash(credentials.passkey, user.passkey):
        if (user.role) == UserRoles.creator:
            return create_access_token(telegram_id=user.telegram_id)
        else:
            raise HTTPException(status_code=401, detail="user is not a creator")
    else:
        raise HTTPException(status_code=401, detail="passkey incorrect")
