"""
tests/test_scorer.py
Unit tests for the scorer service.
Run: pytest tests/test_scorer.py -v
"""

import pytest
from services.scorer import score_quiz

QUESTIONS = [
    {"text": "Q1", "options": ["A", "B", "C", "D"], "correctAnswer": 0, "topic": "Topic A"},
    {"text": "Q2", "options": ["A", "B", "C", "D"], "correctAnswer": 1, "topic": "Topic B"},
    {"text": "Q3", "options": ["A", "B", "C", "D"], "correctAnswer": 2, "topic": "Topic C"},
    {"text": "Q4", "options": ["A", "B", "C", "D"], "correctAnswer": 3, "topic": "Topic A"},
    {"text": "Q5", "options": ["A", "B", "C", "D"], "correctAnswer": 0, "topic": "Topic D"},
]


def test_perfect_score():
    answers = [0, 1, 2, 3, 0]
    result  = score_quiz(QUESTIONS, answers)
    assert result["correct"]    == 5
    assert result["total"]      == 5
    assert result["percentage"] == 100
    assert result["weak_topics"] == []
    assert all(b["correct"] for b in result["breakdown"])


def test_zero_score():
    answers = [3, 0, 0, 0, 3]
    result  = score_quiz(QUESTIONS, answers)
    assert result["correct"]    == 0
    assert result["percentage"] == 0
    assert len(result["weak_topics"]) > 0


def test_partial_score():
    answers = [0, 1, 0, 0, 0]   # Q1, Q2, Q5 correct; Q3, Q4 wrong
    result  = score_quiz(QUESTIONS, answers)
    assert result["correct"]    == 3
    assert result["percentage"] == 60
    assert "Topic C" in result["weak_topics"]
    assert "Topic A" in result["weak_topics"]


def test_weak_topics_deduplicated():
    # Topic A appears in Q1 and Q4 — both wrong
    answers = [3, 1, 2, 0, 0]
    result  = score_quiz(QUESTIONS, answers)
    assert result["weak_topics"].count("Topic A") == 1


def test_breakdown_length():
    answers = [0, 1, 2, 3, 0]
    result  = score_quiz(QUESTIONS, answers)
    assert len(result["breakdown"]) == len(QUESTIONS)


def test_breakdown_content():
    answers = [0, 0, 2, 3, 0]   # Q2 wrong
    result  = score_quiz(QUESTIONS, answers)
    q2_entry = result["breakdown"][1]
    assert q2_entry["correct"]       == False
    assert q2_entry["chosenAnswer"]  == "A"
    assert q2_entry["correctAnswer"] == "B"
    assert q2_entry["topic"]         == "Topic B"
