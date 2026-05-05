"""
Quiz controller.
Orchestrates: data fetch → scoring → grading → AI analysis → persist → respond.
"""

from fastapi import HTTPException
from models.quiz_model import QuizModel
from models.user_model import UserModel
from models.schemas import AnalyzeRequest, AttemptRequest
from services.scorer import score_quiz
from services.grader import compute_grade
from services.analyzer import generate_analysis


# ── Analyze ───────────────────────────────────────────────────────────────────
async def analyze_quiz_controller(payload: AnalyzeRequest):
    quiz    = await QuizModel.find_by_id(payload.quiz_id)
    student = await UserModel.find_by_id(payload.student_id)

    if not quiz:
        raise HTTPException(status_code=404, detail="QUIZ_NOT_FOUND")
    if not student:
        raise HTTPException(status_code=404, detail="STUDENT_NOT_FOUND")
    if not quiz.get("isPublished"):
        raise HTTPException(status_code=403, detail="QUIZ_NOT_PUBLISHED")

    # Enrollment check
    enrolled_ids = [str(e.get("course", "")) for e in student.get("enrolledCourses", [])]
    if str(quiz.get("course")) not in enrolled_ids:
        raise HTTPException(status_code=403, detail="NOT_ENROLLED")

    questions = quiz.get("questions", [])
    if len(payload.answers) != len(questions):
        raise HTTPException(
            status_code=400,
            detail=f"INVALID_ANSWERS: expected {len(questions)} answers, got {len(payload.answers)}",
        )

    # Score
    result = score_quiz(questions, payload.answers)

    # Grade
    grade_info = compute_grade(result["percentage"], quiz.get("passingScore", 60))

    # AI analysis
    ai_analysis = await generate_analysis(
        student_name=student["name"],
        quiz_title=quiz["title"],
        score_result=result,
        grade_info=grade_info,
        passing_score=quiz.get("passingScore", 60),
    )

    # Persist attempt
    await QuizModel.add_attempt(payload.quiz_id, payload.student_id, payload.answers, result["percentage"])

    return {
        "success": True,
        "data": {
            "studentName":       student["name"],
            "quizTitle":         quiz["title"],
            "score": {
                "correct":    result["correct"],
                "total":      result["total"],
                "percentage": result["percentage"],
            },
            "grade":            grade_info["grade"],
            "passed":           grade_info["passed"],
            "passingThreshold": quiz.get("passingScore", 60),
            "weakTopics":       result["weak_topics"],
            "questionBreakdown": result["breakdown"],
            "aiAnalysis":       ai_analysis,
        },
    }


# ── Get quiz ──────────────────────────────────────────────────────────────────
async def get_quiz_controller(quiz_id: str):
    quiz = await QuizModel.find_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="QUIZ_NOT_FOUND")
    # Strip correct answers before returning to client
    safe_questions = [
        {
            "index":   i,
            "text":    q["text"],
            "options": q["options"],
            "points":  q.get("points", 1),
            "topic":   q.get("topic", ""),
        }
        for i, q in enumerate(quiz.get("questions", []))
    ]
    return {
        "success": True,
        "data": {
            "quizId":       str(quiz["_id"]),
            "title":        quiz["title"],
            "passingScore": quiz.get("passingScore", 60),
            "totalQuestions": len(safe_questions),
            "questions":    safe_questions,
        },
    }


# ── Student results ───────────────────────────────────────────────────────────
async def get_student_results_controller(student_id: str):
    student = await UserModel.find_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="STUDENT_NOT_FOUND")

    attempts = await QuizModel.get_attempts_by_student(student_id)
    return {
        "success": True,
        "data": {
            "studentId":   student_id,
            "studentName": student["name"],
            "totalAttempts": len(attempts),
            "attempts":    attempts,
        },
    }


# ── Record attempt (no AI) ────────────────────────────────────────────────────
async def record_attempt_controller(payload: AttemptRequest):
    quiz    = await QuizModel.find_by_id(payload.quiz_id)
    student = await UserModel.find_by_id(payload.student_id)

    if not quiz:
        raise HTTPException(status_code=404, detail="QUIZ_NOT_FOUND")
    if not student:
        raise HTTPException(status_code=404, detail="STUDENT_NOT_FOUND")

    questions = quiz.get("questions", [])
    if len(payload.answers) != len(questions):
        raise HTTPException(status_code=400, detail="INVALID_ANSWERS")

    result    = score_quiz(questions, payload.answers)
    grade_info = compute_grade(result["percentage"], quiz.get("passingScore", 60))

    await QuizModel.add_attempt(payload.quiz_id, payload.student_id, payload.answers, result["percentage"])

    return {
        "success": True,
        "data": {
            "score":   result,
            "grade":   grade_info["grade"],
            "passed":  grade_info["passed"],
            "message": "Attempt recorded. Use /analyze for AI-powered feedback.",
        },
    }
