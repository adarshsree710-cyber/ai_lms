"""
tests/test_grader.py
Unit tests for the grader service.
Run: pytest tests/test_grader.py -v
"""

import pytest
from services.grader import compute_grade


@pytest.mark.parametrize("pct, expected_grade, expected_pass", [
    (100, "A", True),
    (90,  "A", True),
    (89,  "B", True),
    (75,  "B", True),
    (74,  "C", True),
    (60,  "C", True),
    (59,  "D", False),
    (50,  "D", False),
    (49,  "F", False),
    (0,   "F", False),
])
def test_grade_boundaries(pct, expected_grade, expected_pass):
    result = compute_grade(pct, passing_score=60)
    assert result["grade"]  == expected_grade
    assert result["passed"] == expected_pass


def test_custom_passing_score():
    # Passing score of 75
    assert compute_grade(74, passing_score=75)["passed"] == False
    assert compute_grade(75, passing_score=75)["passed"] == True


def test_returns_all_fields():
    result = compute_grade(80)
    assert "grade"      in result
    assert "passed"     in result
    assert "label"      in result
    assert "percentage" in result
