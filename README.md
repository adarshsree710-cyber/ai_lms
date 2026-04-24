# AI LMS Course Recommendation API

FastAPI service for recommending related LMS courses from `data/courses.csv`.

## What It Does

- Accepts a course name in a JSON request body.
- Handles close title matches like `python basic`.
- Returns the closest matching course plus ranked recommendations.
- Exposes interactive Swagger docs at `/docs`.

## Project Structure

```text
ai_lms/
|-- api/
|   `-- main.py
|-- data/
|   `-- courses.csv
|-- models/
|   |-- embedder.py
|   |-- ranker.py
|   `-- recommender.py
|-- tests/
|   |-- test_api.py
|   `-- test_recommender.py
|-- requirements.txt
|-- run_api.bat
`-- README.md
```

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

Preferred command:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

If port `8000` is already in use, run:

```powershell
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8001
```

You can also use:

```powershell
run_api.bat
```

Open the docs:

```text
http://127.0.0.1:8000/docs
```

If you started on port `8001`, open:

```text
http://127.0.0.1:8001/docs
```

Notes:

- On the first run, `sentence-transformers` may download `all-MiniLM-L6-v2`.
- After the model is cached locally, the app prefers the local cache on later runs.
- If `--reload` causes Windows permission errors, leave it off.

## Endpoints

### `GET /`

Health check:

```json
{
  "message": "API running"
}
```

### `POST /recommend`

Request body:

```json
{
  "course": "Python Basics"
}
```

Success response:

```json
{
  "status": "success",
  "data": {
    "course": "Python for Beginners",
    "recommendations": [
      "JavaScript Fundamentals",
      "SQL and Database Design",
      "React Basics"
    ]
  }
}
```

Not found response:

```json
{
  "error": "Course not found"
}
```

## Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

1. Open `POST /recommend`.
2. Select `Try it out`.
3. Paste a request body like:

```json
{
  "course": "python basic"
}
```

4. Select `Execute`.

Useful test cases:

```json
{
  "course": "Python Basics"
}
```

```json
{
  "course": "python basic"
}
```

```json
{
  "course": "random course"
}
```

## Run Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```
