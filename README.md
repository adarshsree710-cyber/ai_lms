# AI LMS Course Recommendation API

FastAPI service for recommending LMS courses from `data/courses.csv`.

## What It Does

- Lists all available courses.
- Recommends ranked courses from a topic or learning goal.
- Supports filters for difficulty, category, and language.
- Handles natural queries like `beginner react`, `build websites`, and small typos like `pyhton`.
- Exposes interactive Swagger docs at `/docs`.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run The API

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Or run:

```powershell
.\run_api.bat
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### `GET /`

Health check and endpoint links.

### `GET /courses`

Returns the full course catalog.

### `GET /recommend`

Use query parameters:

```text
http://127.0.0.1:8000/recommend?query=python&limit=3
```

Optional filters:

```text
difficulty=beginner
category=Programming
language=English
```

### `POST /recommend`

Use this JSON body:

```json
{
  "query": "python basic",
  "limit": 3
}
```

Filtered example:

```json
{
  "query": "react",
  "difficulty": "beginner",
  "limit": 3
}
```

Example response:

```json
{
  "query": "python basic",
  "count": 3,
  "recommendations": [
    {
      "course_id": "C107",
      "title": "Python for Beginners",
      "description": "Introduction to Python programming with hands on exercises",
      "category": "Programming",
      "tags": "python,basics",
      "difficulty": "beginner",
      "duration_hours": 14,
      "instructor": "Meera Pillai",
      "rating": 4.3,
      "total_students": 1100,
      "language": "English"
    }
  ]
}
```

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Open `GET /recommend` or `POST /recommend`.
2. Select `Try it out`.
3. Enter `python`, `python basic`, `beginner react`, or `build websites`.
4. Select `Execute`.

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```
