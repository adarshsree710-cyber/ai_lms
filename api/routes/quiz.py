"""
Quiz routes – mounts all /api/quiz endpoints.
"""

from fastapi import APIRouter, HTTPException, Depends
from api.middleware.auth import verify_token
from api.controllers.quiz_controller import (
    analyze_quiz_controller,
    get_quiz_controller,
    get_student_results_controller,
    record_attempt_controller,
)
from models.schemas import AnalyzeRequest, AttemptRequest

router = APIRouter()


# POST /api/quiz/analyze
@router.post("/analyze", summary="Submit answers and get AI performance analysis")
async def analyze_quiz(payload: AnalyzeRequest, token_data: dict = Depends(verify_token)):
    return await analyze_quiz_controller(payload)


# GET /api/quiz/{quiz_id}
@router.get("/{quiz_id}", summary="Retrieve quiz questions and metadata")
async def get_quiz(quiz_id: str, token_data: dict = Depends(verify_token)):
    return await get_quiz_controller(quiz_id)


# GET /api/quiz/results/{student_id}
@router.get("/results/{student_id}", summary="Get all past quiz results for a student")
async def get_student_results(student_id: str, token_data: dict = Depends(verify_token)):
    return await get_student_results_controller(student_id)


# POST /api/quiz/attempt
@router.post("/attempt", summary="Record quiz attempt without AI analysis")
async def record_attempt(payload: AttemptRequest, token_data: dict = Depends(verify_token)):
    return await record_attempt_controller(payload)
