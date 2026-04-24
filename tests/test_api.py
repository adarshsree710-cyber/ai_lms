import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from api.main import app


class FakeRecommender:
    def find_closest_course(self, query):
        normalized = str(query).strip().lower()
        if normalized in {"python basics", "python basic"}:
            return "Python for Beginners"
        return None

    def get_similar(self, course_title):
        if course_title != "Python for Beginners":
            return None, []

        input_course = {
            "title": "Python for Beginners",
            "difficulty": "beginner",
            "category": "Programming",
        }
        similar = [
            {"title": "SQL and Database Design", "difficulty": "beginner", "category": "Database"},
            {"title": "JavaScript Fundamentals", "difficulty": "beginner", "category": "Programming"},
            {"title": "React Basics", "difficulty": "beginner", "category": "Frontend"},
        ]
        return input_course, similar


class RecommendationApiTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("api.main.get_recommender", return_value=FakeRecommender())
    def test_recommend_endpoint_accepts_close_match(self, _mock_recommender):
        response = self.client.post("/recommend", json={"course": "python basic"})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["course"], "Python for Beginners")
        self.assertIn("recommendations", data["data"])

    @patch("api.main.get_recommender", return_value=FakeRecommender())
    def test_recommend_endpoint_returns_error_for_unknown_course(self, _mock_recommender):
        response = self.client.post("/recommend", json={"course": "random course"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"error": "Course not found"})


if __name__ == "__main__":
    unittest.main()
