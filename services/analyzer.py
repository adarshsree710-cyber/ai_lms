"""
analyzer.py – AI analysis service.
Builds a structured prompt from quiz results and calls the Anthropic Claude API.
Returns the AI-generated performance report as a string.
"""

import anthropic
from config.settings import settings


def _build_prompt(
    student_name: str,
    quiz_title: str,
    score_result: dict,
    grade_info: dict,
    passing_score: int,
) -> str:
    """Construct the analysis prompt dynamically from quiz result data."""

    correct   = score_result["correct"]
    total     = score_result["total"]
    pct       = score_result["percentage"]
    weak      = score_result["weak_topics"]
    breakdown = score_result["breakdown"]
    grade     = grade_info["grade"]
    passed    = grade_info["passed"]

    q_lines = "\n".join(
        f"Q{b['questionIndex'] + 1} [{b['topic']}]: "
        + ("CORRECT" if b["correct"] else f"WRONG (chose \"{b['chosenAnswer']}\", correct: \"{b['correctAnswer']}\")")
        for b in breakdown
    )

    weak_str = ", ".join(weak) if weak else "None — perfect score!"

    return f"""You are an expert educational analyst. A student just completed a quiz.
Provide a personalized, encouraging, and insightful performance analysis.

Student: {student_name}
Quiz: {quiz_title}
Score: {pct}% ({correct}/{total} correct)
Grade: {grade}
Status: {"PASSED" if passed else "FAILED"} (passing threshold: {passing_score}%)
Weak topics (questions answered incorrectly): {weak_str}

Question-by-question breakdown:
{q_lines}

Write a structured analysis with these exact sections:
1. 📊 Performance Summary — brief overall summary with grade context
2. ✅ Strengths — topics where the student did well (skip if all wrong)
3. ⚠️ Weak Areas — specific topics to improve, with a short explanation of why each matters
4. 🚀 Improvement Plan — 3 concrete, actionable study tips tailored to the weak areas
5. 💬 Encouragement — a short motivational closing line

Keep the tone warm, professional, and specific. Address the student by their first name only."""


async def generate_analysis(
    student_name: str,
    quiz_title: str,
    score_result: dict,
    grade_info: dict,
    passing_score: int,
) -> str:
    """
    Call Claude to generate a personalized quiz performance report.

    Returns:
        AI-generated analysis as a plain string.
    Raises:
        Exception if the Anthropic API call fails (caller handles HTTP 502).
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = _build_prompt(student_name, quiz_title, score_result, grade_info, passing_score)

    message = client.messages.create(
        model=settings.AI_MODEL,
        max_tokens=settings.AI_MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text
