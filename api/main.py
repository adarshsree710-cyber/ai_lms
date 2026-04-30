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
    # ── Personalization fields ────────────────────────────────────────────────
    user_level: str | None = Field(
        default=None,
        description="User skill level: beginner, intermediate, or advanced.",
        examples=["beginner"],
    )
    weak_topics: list[str] = Field(
        default=[],
        description="Topics the user struggles with — courses covering these are ranked higher.",
        examples=[["statistics", "loops"]],
    )
    completed_courses: list[str] = Field(
        default=[],
        description="Course titles the user already completed — excluded from results.",
        examples=[["Python for Beginners"]],
    )


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
    from models.ranker import rank_courses
    from models.recommender import Recommender

    # CourseRecommender handles the GET / simple query path.
    # For personalized POST requests, use the embedding-based Recommender
    # so we can attach similarity scores and apply user-level ranking.
    rec = Recommender()
    course_title = rec.find_closest_course(payload.query)

    if course_title is None:
        # Graceful fallback: use TF-IDF recommender without personalization.
        recommendations = recommender.recommend(
            query=payload.query,
            limit=payload.limit,
            difficulty=payload.difficulty or payload.user_level,
            category=payload.category,
            language=payload.language,
        )
        return {
            "query": payload.query,
            "count": len(recommendations),
            "recommendations": recommendations,
        }

    input_course, similar = rec.get_similar(course_title)
    filters = {
        "difficulty": payload.difficulty,
        "category": payload.category,
        "language": payload.language,
    }
    for field_name, expected_value in filters.items():
        if expected_value:
            expected_value = expected_value.strip().lower()
            similar = [
                course
                for course in similar
                if str(course.get(field_name, "")).strip().lower() == expected_value
            ]

    ranked_titles = rank_courses(
        similar,
        input_course=input_course,
        user_level=payload.user_level,
        weak_topics=payload.weak_topics,
        completed_courses=payload.completed_courses,
        limit=payload.limit,
    )

    # Return full course objects so the response matches RecommendationResponse.
    title_set = set(ranked_titles)
    ranked_courses = [c for c in similar if c["title"] in title_set]
    ranked_courses.sort(key=lambda c: ranked_titles.index(c["title"]))
    # Strip internal score key before returning.
    for c in ranked_courses:
        c.pop("_similarity_score", None)

    return {
        "query": payload.query,
        "count": len(ranked_courses),
        "recommendations": ranked_courses,
    }
