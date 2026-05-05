"""
User model – MongoDB CRUD operations via Motor (async).
"""

from bson import ObjectId
from config.database import db


class UserModel:

    @staticmethod
    async def find_by_id(user_id: str) -> dict | None:
        try:
            return await db["users"].find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    @staticmethod
    async def find_by_email(email: str) -> dict | None:
        return await db["users"].find_one({"email": email})

    @staticmethod
    async def get_enrolled_courses(user_id: str) -> list:
        user = await UserModel.find_by_id(user_id)
        if not user:
            return []
        return [str(e.get("course", "")) for e in user.get("enrolledCourses", [])]
