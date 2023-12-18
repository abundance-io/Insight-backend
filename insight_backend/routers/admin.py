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
from ..models.user import User, UserCred, UserRoles
from ..db import UserDB

admin_router = APIRouter()
router = admin_router


@router.post("/admin/")
async def authentiticate_admin(credentials: UserCred):
    try:
        user = await UserDB.objects.get(telegram_id=credentials.telegram_id)
    except NoMatch:
        raise HTTPException(detail="user does not exist", status_code=401)
    user = User(**user.dict())
    if verify_hash(credentials.passkey, user.passkey):
        if (user.role) == UserRoles.admin:
            return create_access_token(telegram_id=user.telegram_id)
        else:
            raise HTTPException(status_code=401, detail="user is not an admin")
    else:
        raise HTTPException(status_code=401, detail="passkey incorrect")


@router.post("/admin/create")
async def create_admin(new_admin: User, user: User = Depends(check_current_user_admin)):
    try:
        new_admin.passkey = hash_password(new_admin.passkey)
        admin = await UserDB(**new_admin.dict()).save()
        return User(**admin.dict())
    except Exception as e:
        if type(e) == UniqueViolationError:
            raise HTTPException(
                status_code=404, detail="telegram user already registered"
            )
        else:
            raise HTTPException(status_code=500, detail="internal server Error")


@router.post("/admin/createcreator")
async def create_creator(creator):
    pass
