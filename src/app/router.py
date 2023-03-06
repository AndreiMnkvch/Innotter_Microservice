from fastapi import Depends
from fastapi.routing import APIRouter
from .dependencies import verify_token
from .dynamodb.db import get_page_stats_db, get_user_stats_db
from fastapi import Depends


router = APIRouter(
    dependencies=[Depends(verify_token)]
)

@router.get("/stats/{user_id}/{page_uuid}")
async def get_page_stats(user_id: int, page_uuid: str):
    return await get_page_stats_db(user_id, page_uuid)

@router.get("/stats/{user_id}")
async def get_user_stats(user_id: int):
    return await get_user_stats_db(user_id)
