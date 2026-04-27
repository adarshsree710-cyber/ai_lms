import unittest

from fastapi.testclient import TestClient

from api.main import app


class RecommendationApiTest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_root_returns_api_links(self):
        response = self.client.get("/")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "AI LMS recommendation API is running")
        self.assertEqual(data["courses_endpoint"], "/courses")
        self.assertEqual(data["docs_endpoint"], "/docs")

    def test_courses_endpoint_returns_catalog(self):
        response = self.client.get("/courses")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(data["count"], 0)
        self.assertIn("title", data["courses"][0])

    def test_recommend_get_returns_ranked_courses(self):
        response = self.client.get("/recommend", params={"query": "python basic", "limit": 3})
        data = response.json()
        titles = [course["title"] for course in data["recommendations"]]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["query"], "python basic")
        self.assertEqual(data["count"], 3)
        self.assertIn("Python for Beginners", titles)

    def test_recommend_post_supports_filters(self):
        response = self.client.post(
            "/recommend",
            json={"query": "react", "difficulty": "beginner", "limit": 3},
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(data["count"], 0)
        self.assertTrue(all(course["difficulty"] == "beginner" for course in data["recommendations"]))


if __name__ == "__main__":
    unittest.main()
