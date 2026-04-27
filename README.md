# AI LMS Frontend

React + Vite frontend for the AI LMS backend.

## Features

- Login and registration
- Protected dashboard with progress chart
- Course listing with filters
- Course details with enroll and mark-complete actions
- Quiz page connected to the backend quiz submission flow
- Shared API client with auth token handling

## Project Structure

```text
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
