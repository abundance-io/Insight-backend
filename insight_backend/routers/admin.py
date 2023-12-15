from fastapi import APIRouter
from ..models.admin import Admin, AdminDB

admin_router = APIRouter()
router = admin_router


@router.post("/admin/")
async def create_admin(new_admin: Admin):
    return await AdminDB(**new_admin.dict()).save()
