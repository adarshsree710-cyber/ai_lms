def rank_courses(
    courses,
    input_course=None,
    user_level=None,
    weak_topics=None,
    completed_courses=None,
    limit=3,
):
    """
    Rank candidate courses using similarity score + optional personalization signals.

    Parameters
    ----------
    courses          : list of course dicts from the recommender stage
    input_course     : the course the user queried (used for category match)
    user_level       : "beginner" / "intermediate" / "advanced"  (optional)
    weak_topics      : list of topic strings the user struggles with (optional)
    completed_courses: list of course titles the user already finished (optional)
    limit            : maximum number of course titles to return
    """
    weak_topics = [t.lower() for t in (weak_topics or [])]
    completed_courses = {c.lower() for c in (completed_courses or [])}

    ranked = []

    for course in courses:
        # Skip courses the user already completed.
        if course["title"].lower() in completed_courses:
            continue

        # ── Base: use the actual semantic similarity from the recommender ──────
        # Falls back to 0.5 when the score wasn't attached (shouldn't happen).
        score = float(course.get("_similarity_score", 0.5))

        # ── Difficulty match ───────────────────────────────────────────────────
        # Prefer: explicit user_level > input_course difficulty as fallback.
        target_level = None
        if user_level:
            target_level = user_level.strip().lower()
        elif input_course:
            target_level = str(input_course.get("difficulty", "")).strip().lower()

        if target_level and course["difficulty"].lower() == target_level:
            score += 0.2

        # ── Category match ────────────────────────────────────────────────────
        if input_course and course["category"] == input_course["category"]:
            score += 0.1

        # ── Weak-topic boost ──────────────────────────────────────────────────
        # Check title and tags so niche matches (e.g. "statistics") surface.
        title_lower = course["title"].lower()
        tags_lower = str(course.get("tags", "")).lower()
        for topic in weak_topics:
            if topic in title_lower or topic in tags_lower:
                score += 0.3

        ranked.append((course["title"], score))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return [title for title, _score in ranked[:limit]]
