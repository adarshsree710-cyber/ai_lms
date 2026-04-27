from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from models.recommender import CourseRecommender


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "courses.csv"

API_DESCRIPTION = """
Search and recommend LMS courses from the local course catalog.

The API reads courses from `data/courses.csv`, ranks matches locally with TF-IDF,
and supports optional filters for difficulty, category, and language.
"""

app = FastAPI(
    title="AI LMS Course Recommendation API",
    description=API_DESCRIPTION,
    version="1.0.0",
    openapi_tags=[
        {"name": "Health", "description": "Basic API status endpoints."},
        {"name": "Courses", "description": "Read-only access to the course catalog."},
        {"name": "Recommendations", "description": "Course search and recommendation endpoints."},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

recommender = CourseRecommender(DATA_PATH)


class Course(BaseModel):
    course_id: str = Field(..., examples=["C107"])
    title: str = Field(..., examples=["Python for Beginners"])
    description: str = Field(..., examples=["Introduction to Python programming with hands on exercises"])
    category: str = Field(..., examples=["Programming"])
    tags: str = Field(..., examples=["python,basics"])
    difficulty: str = Field(..., examples=["beginner"])
    duration_hours: int = Field(..., examples=[14])
    instructor: str = Field(..., examples=["Meera Pillai"])
    rating: float = Field(..., examples=[4.3])
    total_students: int = Field(..., examples=[1100])
    language: str = Field(..., examples=["English"])


class RootResponse(BaseModel):
    message: str
    courses_endpoint: str
    recommend_endpoint: str
    docs_endpoint: str


class CourseListResponse(BaseModel):
    count: int
    courses: list[Course]


class RecommendationResponse(BaseModel):
    query: str
    count: int
    recommendations: list[Course]


class RecommendationRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="Course topic or learning goal, such as `python`, `beginner react`, or `build websites`.",
        examples=["python basic"],
    )
    limit: int = Field(default=5, ge=1, le=10, examples=[3])
    difficulty: str | None = Field(default=None, examples=["beginner"])
    category: str | None = Field(default=None, examples=["Programming"])
    language: str | None = Field(default=None, examples=["English"])


@app.get(
    "/",
    response_model=RootResponse,
    tags=["Health"],
    summary="Check API status",
)
def root():
    return {
        "message": "AI LMS recommendation API is running",
        "courses_endpoint": "/courses",
        "recommend_endpoint": "/recommend?query=python",
        "docs_endpoint": "/docs",
    }


@app.get(
    "/courses",
    response_model=CourseListResponse,
    tags=["Courses"],
    summary="List all courses",
)
def courses():
    return {
        "count": len(recommender.courses),
        "courses": recommender.list_courses(),
    }


@app.get(
    "/recommend",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="Recommend courses with query parameters",
)
def recommend_get(
    query: str = Query(..., min_length=1, examples=["python"]),
    limit: int = Query(default=5, ge=1, le=10, examples=[3]),
    difficulty: str | None = Query(default=None, examples=["beginner"]),
    category: str | None = Query(default=None, examples=["Programming"]),
    language: str | None = Query(default=None, examples=["English"]),
):
    recommendations = recommender.recommend(
        query=query,
        limit=limit,
        difficulty=difficulty,
        category=category,
        language=language,
    )
    return {
        "query": query,
        "count": len(recommendations),
        "recommendations": recommendations,
    }


@app.post(
    "/recommend",
    response_model=RecommendationResponse,
    tags=["Recommendations"],
    summary="Recommend courses with a JSON body",
)
def recommend_post(payload: RecommendationRequest):
    recommendations = recommender.recommend(
        query=payload.query,
        limit=payload.limit,
        difficulty=payload.difficulty,
        category=payload.category,
        language=payload.language,
    )
    return {
        "query": payload.query,
        "count": len(recommendations),
        "recommendations": recommendations,
    }
