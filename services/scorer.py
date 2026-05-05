"""
scorer.py – Pure scoring logic.
Accepts quiz questions and student answers, returns structured result.
No DB or AI calls here — keeps concerns separated.
"""

from typing import List


def score_quiz(questions: List[dict], answers: List[int]) -> dict:
    """
    Score a quiz submission.

    Args:
        questions: list of question dicts from MongoDB (must include 'correctAnswer' and 'topic').
        answers:   list of 0-based chosen option indices from the student.

    Returns:
        dict with keys: correct, total, percentage, weak_topics, breakdown
    """
    correct     = 0
    weak_topics = []
    breakdown   = []

    for i, (q, chosen) in enumerate(zip(questions, answers)):
        correct_answer = q.get("correctAnswer", -1)
        is_correct     = (chosen == correct_answer)
        topic          = q.get("topic", f"Question {i + 1}")

        if is_correct:
            correct += 1
        else:
            weak_topics.append(topic)

        breakdown.append({
            "questionIndex": i,
            "topic":         topic,
            "correct":       is_correct,
            "chosenAnswer":  q["options"][chosen] if 0 <= chosen < len(q["options"]) else "No answer",
            "correctAnswer": q["options"][correct_answer] if 0 <= correct_answer < len(q["options"]) else "",
        })

    total      = len(questions)
    percentage = round((correct / total) * 100) if total > 0 else 0

    return {
        "correct":    correct,
        "total":      total,
        "percentage": percentage,
        "weak_topics": list(dict.fromkeys(weak_topics)),   # deduplicated, order preserved
        "breakdown":  breakdown,
    }
