from ..core.database import db
from ..models.user_model import UserModel


async def create_user(user_data):
    document = user_data.dict()
    await db.db["users"].insert_one(document)
    return document


async def get_user_by_id(user_id: str):
    user = UserModel(**user_id.dict())
    await db.db["users"].find_one({"_id": user_id})
    return user


async def get_user_by_email(email: str):
    user = await db.db["users"].find_one({"email": email})
    return UserModel(**user) if user else None


async def update_user(user_id: str, user_data):
    await db.db["users"].update_one({"_id": user_id}, {"$set" : user_data.dict()})
