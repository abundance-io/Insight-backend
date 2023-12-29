from asyncpg.exceptions import UniqueViolationError
from ormar.exceptions import NoMatch
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from ..models.auth import TokenData
from ..models.course import Course
from ..models.user import User, UserCred, UserRoles, UserList
from ..utils.auth import (
    get_current_user,
    hash_password,
    verify_hash,
    create_access_token,
    check_current_user_admin,
)
from ..db import UserDB, CourseDB

##todo! very important - stop returning user passkeys

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


# dev route todo! - remove in production
@router.post("/dev/admin/create")
async def create_admin(new_admin: User):
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


@router.post("/admin/create")
async def create_admin(
    new_admin: User, check_admin: User = Depends(check_current_user_admin)
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
    new_creator: User, check_admin: User = Depends(check_current_user_admin)
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


@router.delete("/admin/creator/{telegram_id}")
async def delete_creator(
    telegram_id: str, check_admin: User = Depends(check_current_user_admin)
):
    try:
        creator = await UserDB.objects.get(telegram_id=telegram_id)
        if creator.role == UserRoles.creator:
            await UserDB.objects.delete(telegram_id=telegram_id)
            return {"detail": "creator deleted"}
        else:
            raise HTTPException(status_code=400, detail="user is not a creator")
    except NoMatch:
        raise HTTPException(status_code=400, detail="user does not exist")


@router.get("/admin")
async def get_current_admin(check_admin: User = Depends(check_current_user_admin)):
    return check_admin


@router.get("/admin/creator/{telegram_id}")
async def get_creator(
    telegram_id: str, check_admin: User = Depends(check_current_user_admin)
):
    try:
        creator = await UserDB.objects.get(telegram_id=telegram_id)
        if creator.role == UserRoles.creator:
            return User(**creator.dict())
    except NoMatch:
        raise HTTPException(status_code=400, detail="user does not exist")


@router.get("/admin/creator/all")
async def get_all_creators(check_admin: User = Depends(check_current_user_admin)):
    creators = await UserDB.objects.all(role=UserRoles.creator)
    creators = [User(**creator.dict()) for creator in creators]
    return UserList(**{"users": creators})


@router.post("/admin/create/course/")
async def create_course(
    new_course: Course, check_admin: User = Depends(check_current_user_admin)
):
    try:
        # remove spaces and make lower case
        new_course.course_code = new_course.course_code.lower().replace(" ", "")
        course = await CourseDB(**new_course.dict()).save()
        return Course(**course.dict())

    except UniqueViolationError:
        raise HTTPException(status_code=400, detail="course already created")
