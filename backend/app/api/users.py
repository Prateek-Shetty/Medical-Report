from fastapi import APIRouter, Request
from bson import ObjectId

router = APIRouter()

@router.get("/")
async def get_all_users(request: Request):
    db = request.app.state.db
    users = await db.users.find().to_list(100)
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@router.get("/{user_id}")
async def get_user(user_id: str, request: Request):
    db = request.app.state.db
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}
    user["_id"] = str(user["_id"])
    return user
