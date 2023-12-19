from asyncpg.exceptions import UniqueViolationError
from ormar.exceptions import NoMatch
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from ..models.auth import TokenData

from ..models.user import User, UserCred, UserRoles, UserBase, UserList
from ..utils.auth import (
    get_current_user,
    hash_password,
    verify_hash,
    create_access_token,
    check_current_user_admin,
)
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
async def create_admin(
    new_admin: User, admin: User = Depends(check_current_user_admin)
):
    if new_admin.role == UserRoles.admin:
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
    else:
        raise HTTPException(status_code=400, detail="user is not an admin")


@router.post("/admin/create/creator")
async def create_creator(
    new_creator: User, admin: User = Depends(check_current_user_admin)
):
    if new_creator.role == UserRoles.creator:
        try:
            new_creator.passkey = hash_password(new_creator.passkey)
            admin = await UserDB(**new_creator.dict()).save()
            return User(**admin.dict())
        except Exception as e:
            if type(e) == UniqueViolationError:
                raise HTTPException(
                    status_code=404, detail="telegram user already registered"
                )
            else:
                raise HTTPException(status_code=500, detail="internal server Error")
    else:
        raise HTTPException(status_code=400, detail="user is not a creator")


@router.delete("/admin/creator")
async def delete_creator(
    creator_del: UserBase, admin: User = Depends(check_current_user_admin)
):
    try:
        creator = await UserDB.objects.get(telegram_id=creator_del.telegram_id)
        if creator.role == UserRoles.creator:
            await UserDB.objects.delete(telegram_id=creator_del.telegram_id)
            return {"detail": "creator deleted"}
        else:
            raise HTTPException(status_code=400, detail="user is not a creator")
    except NoMatch:
        raise HTTPException(status_code=400, detail="user does not exist")


@router.get("/admin/creator")
async def get_creator(
    creator_get: UserBase, admin: User = Depends(check_current_user_admin)
):
    try:
        creator = await UserDB.objects.get(telegram_id=creator_get.telegram_id)
        if creator.role == UserRoles.creator:
            return User(**creator.dict())
    except NoMatch:
        raise HTTPException(status_code=400, detail="user does not exist")


@router.get("/admin/creator/all")
async def get_all_creators(admin: User = Depends(check_current_user_admin)):
    creators = await UserDB.objects.all(role=UserRoles.creator)
    creators = [User(**creator.dict()) for creator in creators]
    return UserList(**{"users": creators})
