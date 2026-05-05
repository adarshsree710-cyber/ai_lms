# AI LMS – Quiz Performance Analyzer

AI-powered student quiz analysis built with **FastAPI** + **MongoDB** + **Anthropic Claude**.

When a student completes a quiz, this service scores their answers, detects weak topics, computes a letter grade, and returns a personalized AI-generated feedback report.

---

## Project structure

```
AI_LMS_Quiz_Analysis/
├── api/
│   ├── main.py                  # FastAPI app, CORS, route mounting
│   ├── routes/
│   │   ├── quiz.py              # /api/quiz/* endpoints
│   │   └── health.py            # /api/health
│   ├── middleware/
│   │   └── auth.py              # JWT Bearer token verification
│   └── controllers/
│       └── quiz_controller.py   # Business logic orchestration
├── models/
│   ├── schemas.py               # Pydantic request/response models
│   ├── quiz_model.py            # MongoDB Quiz CRUD (Motor async)
│   └── user_model.py            # MongoDB User CRUD (Motor async)
├── services/
│   ├── scorer.py                # Pure quiz scoring logic
│   ├── grader.py                # Letter grade computation
│   └── analyzer.py              # Claude AI prompt + API call
├── config/
│   ├── settings.py              # Pydantic settings (reads .env)
│   └── database.py              # Motor async MongoDB client
├── data/
│   ├── quizzes.csv              # Seed data – 13 quizzes
│   ├── users.csv                # Seed data – students & instructors
│   └── seed.py                  # Database seeder script
├── tests/
│   ├── test_scorer.py           # Unit tests – scorer service
│   └── test_grader.py           # Unit tests – grader service
├── .env.example                 # Environment variable template
├── .gitignore
├── requirements.txt
├── run_api.bat                  # Windows launcher
└── run_api.sh                   # Linux/Mac launcher
```

---

## Quickstart

### 1. Clone and create virtual environment
```bash
git clone <repo-url>
cd AI_LMS_Quiz_Analysis
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env — fill in MONGODB_URI, JWT_SECRET, and ANTHROPIC_API_KEY
```

### 4. Seed the database
```bash
python data/seed.py
```

### 5. Run the server
```bash
# Windows
run_api.bat

# Linux/Mac
bash run_api.sh

# Or directly:
uvicorn api.main:app --reload --port 8000
```

### 6. Open API docs
```
http://localhost:8000/docs
```

---

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/quiz/analyze` | Submit answers → AI performance report |
| GET | `/api/quiz/{quiz_id}` | Get quiz questions (no correct answers) |
| GET | `/api/quiz/results/{student_id}` | Student's full attempt history |
| POST | `/api/quiz/attempt` | Record attempt without AI analysis |

All endpoints except `/api/health` require `Authorization: Bearer <jwt_token>`.

### POST /api/quiz/analyze – request body
```json
{
  "studentId": "69f43975b1f44561851e9043",
  "quizId":    "661c00000000000000000101",
  "answers":   [0, 1, 2, 1, 0, 1, 2, 1, 0, 2]
}
```

### Response
```json
{
  "success": true,
  "data": {
    "studentName": "Rahul Nair",
    "quizTitle":   "MERN Stack Bootcamp Final Quiz",
    "score":       { "correct": 7, "total": 10, "percentage": 70 },
    "grade":       "B",
    "passed":      true,
    "passingThreshold": 60,
    "weakTopics":  ["React hooks", "HTTP methods", "Node.js setup"],
    "questionBreakdown": [...],
    "aiAnalysis":  "📊 Performance Summary\n..."
  }
}
```

---

## Running tests
```bash
pytest tests/ -v
```

---

## Grading scale

| Grade | Range | Status |
|-------|-------|--------|
| A | 90–100% | Pass |
| B | 75–89% | Pass |
| C | 60–74% | Pass |
| D | 50–59% | Fail |
| F | <50% | Fail |

---

## Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/elearning` |
| `JWT_SECRET` | Secret for JWT signing | — |
| `ANTHROPIC_API_KEY` | Claude API key (from AI/ML team) | — |
| `AI_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |
| `AI_MAX_TOKENS` | Max tokens in AI response | `1000` |
| `PORT` | Server port | `8000` |
| `ALLOWED_ORIGINS` | CORS allowed origins (JSON array) | localhost:3000, 5173 |

> ⚠️ Never commit `.env` or expose `ANTHROPIC_API_KEY` to the client/browser.
