from fastapi import APIRouter

from app.router.v1.user_router import router as v1_user_router
from app.router.v1.sms_router import router as v1_sms_router

router = APIRouter()

router.include_router(v1_user_router, tags=["USER"])
router.include_router(v1_sms_router, tags=["SMS"])
