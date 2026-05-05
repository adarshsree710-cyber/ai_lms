"""
grader.py – Grade computation logic.
Converts a percentage score into a letter grade and pass/fail status.
"""


GRADE_SCALE = [
    (90, "A", "Excellent"),
    (75, "B", "Good"),
    (60, "C", "Satisfactory"),
    (50, "D", "Below threshold"),
    (0,  "F", "Insufficient"),
]


def compute_grade(percentage: float, passing_score: int = 60) -> dict:
    """
    Compute letter grade and pass/fail from a percentage score.

    Args:
        percentage:    score percentage (0–100).
        passing_score: minimum percentage required to pass (default 60).

    Returns:
        dict with keys: grade, passed, label, percentage
    """
    grade = "F"
    label = "Insufficient"

    for threshold, letter, desc in GRADE_SCALE:
        if percentage >= threshold:
            grade = letter
            label = desc
            break

    return {
        "grade":      grade,
        "passed":     percentage >= passing_score,
        "label":      label,
        "percentage": percentage,
    }
