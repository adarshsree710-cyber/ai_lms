"""
Pydantic schemas for request validation and response shaping.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    student_id: str = Field(..., alias="studentId", description="MongoDB ObjectId of the student")
    quiz_id:    str = Field(..., alias="quizId",    description="MongoDB ObjectId of the quiz")
    answers:    List[int] = Field(..., description="0-based option indices, one per question")

    class Config:
        populate_by_name = True


class AttemptRequest(BaseModel):
    student_id: str = Field(..., alias="studentId")
    quiz_id:    str = Field(..., alias="quizId")
    answers:    List[int]

    class Config:
        populate_by_name = True


class ScoreResult(BaseModel):
    correct:    int
    total:      int
    percentage: float
    weak_topics: List[str]
    breakdown:  List[dict]


class GradeInfo(BaseModel):
    grade:  str
    passed: bool
    label:  str


class AnalyzeResponse(BaseModel):
    success:     bool
    studentName: str
    quizTitle:   str
    score:       dict
    grade:       str
    passed:      bool
    passingThreshold: int
    weakTopics:  List[str]
    questionBreakdown: List[dict]
    aiAnalysis:  str
