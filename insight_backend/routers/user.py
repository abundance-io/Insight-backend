from asyncpg.exceptions import UniqueViolationError
from ormar.exceptions import NoMatch
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from ..models.auth import TokenData
from ..models.content import Course
from ..models.user import User, UserCred, UserRoles, UserList, UserPending
from ..utils.auth import (
    get_current_user,
    hash_password,
    verify_hash,
    create_access_token,
    check_current_user_admin,
)
from ..db import CreatorsDB, UserDB, CourseDB, UserPendingDB


user_router = APIRouter()
router = user_router


@router.post("/user/poll/")
async def create_creator(new_user: User):
    try:
        pending_user = await UserPendingDB.objects.get(
            telegram_repr=new_user.telegram_repr
        )
        if pending_user.role == new_user.role:
            try:
                new_user.passkey = hash_password(new_user.passkey)
                user = await UserDB(**new_user.dict()).save()
                if user.role == UserRoles.creator:
                    #add creator profile
                    profile =  CreatorsDB(user=user)
                    await user.creator_profile.add(profile)
                await UserPendingDB.objects.delete(telegram_repr=new_user.telegram_repr)
                return User(**user.dict())
            except Exception as e:
                if type(e) == UniqueViolationError:
                    raise HTTPException(
                        status_code=404, detail="telegram user already registered"
                    )
                else:
                    raise HTTPException(status_code=500, detail="internal server Error")
        else:
            raise HTTPException(
                status_code=400, detail="tried to poll with unassigned role"
            )
    except NoMatch:
        raise HTTPException(status_code=404, detail="user is not pending")
