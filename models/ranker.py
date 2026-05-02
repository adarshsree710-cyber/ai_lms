def rank_courses(courses, input_course=None):
    ranked = []

    for course in courses:
        score = 0

        # Base similarity from the recommender stage.
        score += 0.6

        if input_course is not None:
            if course["difficulty"] == input_course["difficulty"]:
                score += 0.2

            if course["category"] == input_course["category"]:
                score += 0.2

        ranked.append((course["title"], score))

    ranked.sort(key=lambda item: item[1], reverse=True)

    return [course_title for course_title, _score in ranked[:3]]
