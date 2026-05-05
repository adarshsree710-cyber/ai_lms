@echo off
echo Starting AI LMS Quiz Performance Analyzer...
call .venv\Scripts\activate
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
