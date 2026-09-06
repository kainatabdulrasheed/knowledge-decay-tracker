# Knowledge Decay Tracker

Django app to write notes, generate/take AI-powered MCQ tests per topic, and track scores over time.

## Status
Core app + REST API + AI test generation complete. Auth in progress. No deployment yet.

## Tech stack
Python, Django, Django REST Framework, PostgreSQL, Google Gemini API, Django Templates (no separate frontend)

## Setup
1. Clone repo, create venv, activate
2. `pip install -r requirements.txt`
3. Create PostgreSQL database + user, set values in `.env` (see `.env.example`)
4. Get a Gemini API key from Google AI Studio, add it to `.env`
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`
8. Log in via `/admin`, add Topics/Notes, then use the app at `/`

## Features (Phase 1)
- Notes organized by Topic
- MCQ test-taking with automatic scoring
- Test review + history per topic and globally

## Features (Phase 2)
- REST API (`/api/`) for topics, notes, tests, and attempts
- Full CRUD via API (GET, POST, PUT, PATCH, DELETE)

## Features (Phase 3)
- AI-generated MCQ tests from your notes (`POST /api/topics/<id>/generate-test/`), powered by Google Gemini

## Roadmap
- Phase 4: Authentication (token-based)
- Phase 5: Deployment + polish