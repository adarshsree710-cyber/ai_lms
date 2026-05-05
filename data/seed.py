"""
data/seed.py
Seeds the MongoDB database with quiz and user data from the CSV files.
Run once: python data/seed.py
"""

import asyncio
import csv
import ast
import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/elearning"
client    = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db        = client["elearning"]


def parse_questions(raw: str) -> list:
    """Parse the Python-literal questions column from the CSV."""
    try:
        return ast.literal_eval(raw)
    except Exception as e:
        print(f"  Warning: could not parse questions — {e}")
        return []


TOPIC_MAP = {
    "MERN Stack Bootcamp Final Quiz": [
        "MERN fundamentals", "MongoDB", "React", "Node.js", "Express.js",
        "React hooks", "Express.js routing", "Node.js setup", "MongoDB integration", "HTTP methods",
    ],
    "React Basics Quiz": [
        "React basics", "React history", "JSX", "useState hook", "useEffect hook",
        "Props", "List rendering", "Keys in React", "useEffect hook", "Components",
    ],
    "Advanced React Patterns Quiz": [
        "React.memo", "useMemo", "useCallback", "Context API", "HOC",
        "Render Props", "useRef", "Code splitting", "useReducer", "Suspense",
    ],
    "Node.js & Express API Quiz": [
        "Node.js basics", "npm", "Express setup", "Routing", "Middleware",
        "REST methods", "Error handling", "Async/Await", "Environment variables", "nodemon",
    ],
    "MongoDB & Mongoose Quiz": [
        "MongoDB basics", "Documents", "Collections", "Mongoose schemas", "CRUD",
        "Querying", "Indexing", "References", "Aggregation", "Validation",
    ],
    "JavaScript ES6+ Quiz": [
        "let/const", "Arrow functions", "Destructuring", "Spread/Rest", "Template literals",
        "Promises", "Async/Await", "Modules", "Classes", "Map/Filter/Reduce",
    ],
    "Python for Beginners Quiz": [
        "Python basics", "Variables", "Data types", "Loops", "Functions",
        "Lists", "Dictionaries", "File I/O", "OOP basics", "Error handling",
    ],
    "Data Structures & Algorithms Quiz": [
        "Arrays", "Linked lists", "Stacks", "Queues", "Trees",
        "Sorting", "Searching", "Big O notation", "Hash maps", "Graphs",
    ],
    "Deep Learning with TensorFlow Quiz": [
        "TensorFlow basics", "Google/TF history", "Neural networks", "Keras", "Activation functions",
        "ReLU", "Epochs", "Optimizers", "Overfitting", "model.fit",
    ],
    "UI UX Design Fundamentals Quiz": [
        "UI definition", "UX definition", "UI vs UX", "UX focus", "Wireframes",
        "Affordance", "Prototyping", "Contrast", "User research", "Design tools",
    ],
    "Full Stack Project Development Quiz": [
        "Full stack definition", "Frontend tech", "Database tech", "Express.js role", "HTTP methods",
        "Authentication", "Version control", "REST APIs", "Environment variables", "Deployment",
    ],
    "SQL and Database Design Quiz": [
        "SQL basics", "SELECT queries", "INSERT queries", "Primary keys", "Foreign keys",
        "WHERE clause", "Aggregate functions", "Normalization", "SQL JOINs", "UPDATE queries",
    ],
    "DevOps & Cloud Fundamentals Quiz": [
        "DevOps basics", "CI/CD", "Docker", "Kubernetes", "Cloud providers",
        "Infrastructure as Code", "Monitoring", "Version control", "Microservices", "Deployment strategies",
    ],
}


async def seed_quizzes():
    print("[Seed] Seeding quizzes...")
    await db["quizzes"].drop()

    with open("data/quizzes.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions_raw = parse_questions(row["questions"])
            title         = row["title"].strip()
            topics        = TOPIC_MAP.get(title, [])

            questions = []
            for i, q in enumerate(questions_raw):
                questions.append({
                    "text":          q["text"],
                    "options":       q["options"],
                    "correctAnswer": q["correctAnswer"],
                    "points":        q.get("points", 1),
                    "topic":         topics[i] if i < len(topics) else f"Topic {i + 1}",
                })

            doc = {
                "_id":         ObjectId(row["course"].strip()),   # use course id as quiz _id for demo
                "title":       title,
                "course":      ObjectId(row["course"].strip()),
                "createdBy":   ObjectId(row["createdBy"].strip()),
                "questions":   questions,
                "passingScore": int(row["passingScore"]),
                "isPublished": row["isPublished"].strip() == "True",
                "attempts":    [],
                "createdAt":   datetime.utcnow(),
            }
            await db["quizzes"].insert_one(doc)
            print(f"  ✓ {title}")

    print(f"[Seed] {await db['quizzes'].count_documents({})} quizzes seeded.\n")


async def seed_users():
    print("[Seed] Seeding users...")
    await db["users"].drop()

    with open("data/users.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            enrolled_raw = row.get("enrolledCourses", "[]").strip()
            teaching_raw = row.get("teachingCourses", "[]").strip()

            try:
                enrolled_list_raw = ast.literal_eval(enrolled_raw) if enrolled_raw else []
                enrolled = [{"course": ObjectId(str(e["course"]).replace("ObjectId('", "").replace("')", ""))} for e in enrolled_list_raw]
            except Exception:
                enrolled = []

            try:
                teaching_list_raw = ast.literal_eval(teaching_raw) if teaching_raw else []
                teaching = [ObjectId(str(t).replace("ObjectId('", "").replace("')", "")) for t in teaching_list_raw]
            except Exception:
                teaching = []

            doc = {
                "name":            row["name"].strip(),
                "email":           row["email"].strip(),
                "password":        row["password"].strip(),   # plain for seed only — hash in prod
                "role":            row["role"].strip(),
                "enrolledCourses": enrolled,
                "teachingCourses": teaching,
                "isActive":        row["isActive"].strip() == "True",
                "createdAt":       datetime.utcnow(),
            }
            await db["users"].insert_one(doc)

    print(f"[Seed] {await db['users'].count_documents({})} users seeded.\n")


async def main():
    print("=" * 50)
    print("  AI LMS – Database Seeder")
    print("=" * 50)
    await seed_quizzes()
    await seed_users()
    print("[Seed] Done. Database is ready.")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
