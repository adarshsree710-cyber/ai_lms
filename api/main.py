from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel

from models.ranker import rank_courses
from models.recommender import Recommender


app = FastAPI()


class RequestData(BaseModel):
    course: str


@lru_cache
def get_recommender():
    return Recommender()


@app.get("/")
def home():
    return {"message": "API running"}


@app.post("/recommend")
def recommend(data: RequestData):
    rec = get_recommender()
    course = rec.find_closest_course(data.course)

    if course is None:
        return {"error": "Course not found"}

    input_course, similar = rec.get_similar(course)
    final = rank_courses(similar, input_course)

    return {
        "status": "success",
        "data": {
            "course": course,
            "recommendations": final,
        },
    }
