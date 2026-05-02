<<<<<<< HEAD
# AI LMS Frontend

React + Vite frontend for the AI LMS backend.

## Features

- Login and registration
- Protected dashboard with progress chart
- Course listing with filters
- Course details with enroll and mark-complete actions
- Quiz page connected to the backend quiz submission flow
- Shared API client with auth token handling
=======
# AI LMS Course Recommendation API

FastAPI service for recommending related LMS courses from `data/courses.csv`.

## What It Does

- Accepts a course name in a JSON request body.
- Handles close title matches like `python basic`.
- Returns the closest matching course plus ranked recommendations.
- Exposes interactive Swagger docs at `/docs`.
>>>>>>> 429b1a044475f29da7078dcf42be85b2a33dad83

## Project Structure

```text
<<<<<<< HEAD
ai-lms-frontend/
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── README.md
├── vite.config.js
└── src/
    ├── App.jsx
    ├── main.jsx
    ├── styles.css
    ├── components/
    │   ├── Layout.jsx
    │   ├── ProtectedRoute.jsx
    │   └── StatCard.jsx
    ├── context/
    │   └── AuthContext.jsx
    ├── lib/
    │   └── api.js
    └── pages/
        ├── CourseDetailsPage.jsx
        ├── CoursesPage.jsx
        ├── DashboardPage.jsx
        ├── LoginPage.jsx
        ├── QuizPage.jsx
        └── RegisterPage.jsx
```

## Requirements

- Node.js 18+
- Running AI LMS backend at `http://localhost:5000`

## Setup

```bash
npm install
```

If PowerShell blocks `npm`, use:

```bash
npm.cmd install
```

## Environment

Create a `.env` file from `.env.example`.

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Default environment value:

```env
VITE_API_URL=http://localhost:5000/api
```

## Run

```bash
npm run dev
```

Or on Windows PowerShell:

```powershell
npm.cmd run dev
```

Frontend dev server:

- `http://localhost:5173`

## Build

```bash
npm run build
```

## Backend Notes

- Auth routes use `/login`, `/register`, and `/me`
- Courses use `/courses` and `/courses/:id`
- Progress uses `/progress`, `/progress/complete`, and `/progress/ai-recommendation`
- Quiz uses `/quiz` and `/quiz/:id`

## Demo Accounts

- Student: `student@ailms.com` / `password123`
- Instructor: `instructor@ailms.com` / `password123`
- Admin: `admin@ailms.com` / `password123`

## Zip Ready

When sharing this project, include:

- `src/`
- `index.html`
- `package.json`
- `vite.config.js`
- `README.md`
- `.env.example`
- `.gitignore`

Do not include:

- `node_modules/`
- `dist/`
- `.env`
=======
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
>>>>>>> 429b1a044475f29da7078dcf42be85b2a33dad83
