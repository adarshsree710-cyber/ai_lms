"""
Quiz model – MongoDB CRUD operations via Motor (async).
"""

from bson import ObjectId
from datetime import datetime
from config.database import db


class QuizModel:

    @staticmethod
    async def find_by_id(quiz_id: str) -> dict | None:
        try:
            return await db["quizzes"].find_one({"_id": ObjectId(quiz_id)})
        except Exception:
            return None

    @staticmethod
    async def add_attempt(quiz_id: str, student_id: str, answers: list, score: float):
        attempt = {
            "student":     ObjectId(student_id),
            "answers":     answers,
            "score":       score,
            "submittedAt": datetime.utcnow(),
        }
        await db["quizzes"].update_one(
            {"_id": ObjectId(quiz_id)},
            {"$push": {"attempts": attempt}},
        )

    @staticmethod
    async def get_attempts_by_student(student_id: str) -> list:
        """Return all quiz attempts across all quizzes for a student."""
        pipeline = [
            {"$unwind": "$attempts"},
            {"$match": {"attempts.student": ObjectId(student_id)}},
            {
                "$project": {
                    "quizTitle": "$title",
                    "score":     "$attempts.score",
                    "submittedAt": "$attempts.submittedAt",
                }
            },
            {"$sort": {"submittedAt": -1}},
        ]
        cursor  = db["quizzes"].aggregate(pipeline)
        results = []
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    @staticmethod
    async def list_published() -> list:
        cursor = db["quizzes"].find({"isPublished": True}, {"questions.correctAnswer": 0})
        quizzes = []
        async for q in cursor:
            q["_id"] = str(q["_id"])
            quizzes.append(q)
        return quizzes
