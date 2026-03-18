# Agent Changelog

All changes made by Claude Code are logged here with timestamps and descriptions.

---

## [2026-03-19] Project Initialization

### Decisions Made
- **Platform**: Web + Mobile (both)
- **Backend Framework**: Flask (Python)
- **AI Assistant**: Included in V1
- **Social Features**: Included in V1
- **Hosting**: Deferred until product is complete

### Changes
- `Agent.md` — Created this changelog file to track all modifications

---

## [2026-03-19] Flask Backend — Project Structure & Database Schema

### Architecture
- **Pattern**: App factory with Blueprints
- **Layers**: Routes (thin) → Services (business logic) → Models (data)
- **Auth**: JWT (access + refresh tokens) with token blocklist

### Files Created (55 files total)

**Config & Entry**
- `backend/config.py` — Dev/Test/Prod configuration classes
- `backend/run.py` — App entry point
- `backend/requirements.txt` — Python dependencies
- `backend/.env.example` — Environment variable template
- `backend/.flaskenv` — Flask CLI config

**App Core**
- `backend/app/__init__.py` — App factory (create_app)
- `backend/app/extensions.py` — SQLAlchemy, JWT, Marshmallow, CORS, Limiter instances

**Models (10 models)**
- `backend/app/models/user.py` — User + UserProfile (auth, public profiles, streaks)
- `backend/app/models/challenge.py` — Challenge (75-day, difficulty, state machine)
- `backend/app/models/task.py` — Task (5-8 per challenge, categorized)
- `backend/app/models/daily_log.py` — DailyLog (per-day tracking hub)
- `backend/app/models/task_completion.py` — TaskCompletion (task × day join)
- `backend/app/models/proof.py` — Proof (image uploads linked to tasks)
- `backend/app/models/ai_chat.py` — AIConversation + AIMessage
- `backend/app/models/social.py` — Follow + SharedUpdate
- `backend/app/models/token_blocklist.py` — JWT blocklist for logout

**Schemas (Marshmallow serialization)**
- `backend/app/schemas/` — 7 schema files for all models

**API Blueprints (7 modules)**
- `backend/app/api/auth/` — Register, Login, Refresh, Logout, Me
- `backend/app/api/challenges/` — Create, Active, History, Get by ID
- `backend/app/api/tasks/` — List tasks for active challenge
- `backend/app/api/progress/` — Today, Complete task, Skip, Dashboard, History
- `backend/app/api/proofs/` — Upload proof, Get proofs by day
- `backend/app/api/ai/` — Chat, List conversations, Get conversation
- `backend/app/api/social/` — Profile, Share update, Feed, Follow, Unfollow

**Services (business logic)**
- `backend/app/services/auth_service.py` — Registration, login, logout
- `backend/app/services/challenge_service.py` — Challenge creation, state management
- `backend/app/services/progress_service.py` — Task completion, streaks, dashboard
- `backend/app/services/proof_service.py` — Image upload and validation
- `backend/app/services/ai_service.py` — Claude API integration for coaching
- `backend/app/services/social_service.py` — Follow system, feed, sharing

**Utils**
- `backend/app/utils/enums.py` — All shared enums (Difficulty, Status, Category, etc.)
- `backend/app/utils/errors.py` — Custom exceptions + error handlers
- `backend/app/utils/decorators.py` — @active_challenge_required
- `backend/app/utils/file_upload.py` — Local file upload handler
- `backend/app/utils/state_machine.py` — Challenge state transitions

**Jobs**
- `backend/app/jobs/daily_checker.py` — End-of-day evaluation (mark missed, advance days)

**Tests**
- `backend/tests/conftest.py` — Pytest fixtures (app, db, client)

### Database Schema Summary

```
User 1──1 UserProfile
User 1──* Challenge
User 1──* AIConversation
User 1──* SharedUpdate
User *──* User (via Follow)

Challenge 1──* Task
Challenge 1──* DailyLog

DailyLog 1──* TaskCompletion
DailyLog 1──* Proof

Task 1──* TaskCompletion
TaskCompletion 1──0..1 Proof
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login |
| POST | /api/auth/refresh | Refresh access token |
| POST | /api/auth/logout | Logout (blocklist token) |
| GET | /api/auth/me | Get current user |
| POST | /api/challenges | Create challenge |
| GET | /api/challenges/active | Get active challenge |
| GET | /api/challenges/:id | Get challenge by ID |
| GET | /api/challenges/history | Get past challenges |
| GET | /api/tasks | Get tasks for active challenge |
| GET | /api/progress/today | Get/create today's log |
| POST | /api/progress/complete-task | Mark task done |
| POST | /api/progress/skip | Skip today |
| GET | /api/progress/dashboard | Dashboard data |
| GET | /api/progress/history | All daily logs |
| POST | /api/proofs/upload | Upload proof image |
| GET | /api/proofs/day/:n | Get proofs for day N |
| POST | /api/ai/chat | Chat with AI coach |
| GET | /api/ai/conversations | List conversations |
| GET | /api/ai/conversations/:id | Get conversation |
| GET | /api/social/profile/:username | Public profile |
| POST | /api/social/share | Share an update |
| GET | /api/social/feed | Get followed users' updates |
| POST | /api/social/follow/:id | Follow user |
| POST | /api/social/unfollow/:id | Unfollow user |

---

## [2026-03-19] Backend Boot Test — PASSED

- Python 3.14.3, all dependencies installed in `backend/venv`
- Flask app creates successfully with **27 routes**
- SQLite database created with **12 tables**
- All models, blueprints, services, and schemas load without errors

---

## [2026-03-19] React Frontend — Scaffolded & Built

### Tech
- Vite + React 19, Tailwind CSS v4, React Router v7
- Zustand (state), React Query (server state), Axios (API)
- Proxy configured: `/api` → Flask backend at `localhost:5000`

### Files Created

**Config**
- `frontend/vite.config.js` — Vite config with Tailwind plugin + API proxy
- `frontend/src/index.css` — Tailwind import

**API Services (7 files)**
- `frontend/src/services/api.js` — Axios instance with JWT interceptors + auto-refresh
- `frontend/src/services/auth.js` — Register, login, logout, me
- `frontend/src/services/challenges.js` — Create, getActive, getById, history
- `frontend/src/services/progress.js` — Today, completeTask, skip, dashboard, history
- `frontend/src/services/proofs.js` — Upload (multipart), getByDay
- `frontend/src/services/ai.js` — Chat, getConversations, getConversation
- `frontend/src/services/social.js` — Profile, share, feed, follow, unfollow

**Zustand Stores (2 files)**
- `frontend/src/store/authStore.js` — Auth state, login/register/logout actions
- `frontend/src/store/challengeStore.js` — Challenge, dashboard, today log, task completion

**Layout & Common (4 files)**
- `frontend/src/components/layout/Navbar.jsx` — Top nav with auth-aware links
- `frontend/src/components/layout/Layout.jsx` — Shell with Outlet
- `frontend/src/components/common/ProtectedRoute.jsx` — Auth guard
- `frontend/src/components/common/LoadingSpinner.jsx` — Spinner

**Pages (7 files)**
- `frontend/src/pages/Home.jsx` — Landing page with feature cards
- `frontend/src/pages/Login.jsx` — Login form
- `frontend/src/pages/Register.jsx` — Registration form with confirm password
- `frontend/src/pages/Dashboard.jsx` — Main dashboard (progress ring, stats, checklist)
- `frontend/src/pages/NewChallenge.jsx` — Challenge creation (difficulty, tasks)
- `frontend/src/pages/AICoach.jsx` — Chat interface with AI coach
- `frontend/src/pages/Feed.jsx` — Social feed of followed users' updates

**Dashboard Components (3 files)**
- `frontend/src/components/dashboard/ProgressRing.jsx` — SVG circular progress
- `frontend/src/components/dashboard/StatsBar.jsx` — Streak, completed, skips, failures
- `frontend/src/components/dashboard/TodayChecklist.jsx` — Task list with completion + proof upload

**Proof Component**
- `frontend/src/components/proofs/ProofUpload.jsx` — Image upload per task

### Build Test — PASSED
- `vite build` completes in 308ms
- Dev server starts on port 3000, returns HTTP 200

---

## [2026-03-19] Docker Setup — Full Stack Containerized

### Files Created
- `docker-compose.yml` — 4 services: PostgreSQL 16, Redis 7, Flask backend (Gunicorn 4 workers), React frontend (Nginx)
- `docker-compose.dev.yml` — Dev mode: only DB + Redis containers, run Flask/Vite on host
- `backend/Dockerfile` — Python 3.12-slim, pip install, entrypoint with DB init + Gunicorn
- `backend/entrypoint.sh` — Creates DB tables on startup, launches Gunicorn
- `backend/.dockerignore` — Excludes venv, __pycache__, .env, uploads
- `frontend/Dockerfile` — Multi-stage: Node 20 build → Nginx Alpine serve
- `frontend/nginx.conf` — SPA routing, API proxy to backend:5000, gzip, asset caching
- `frontend/.dockerignore` — Excludes node_modules, dist
- `.env` — Root env vars for docker-compose

### Fixes During Setup
- Pinned `marshmallow>=3,<4` (v4 broke flask-marshmallow pprint import)
- Added `redis` Python package (Flask-Limiter needs it for Redis storage)
- Fixed UserProfileSchema exclude field (marshmallow-sqlalchemy doesn't allow exclude in Nested)

### Verification — ALL PASSED
- All 4 containers running: db (healthy), redis (healthy), backend (up), frontend (up)
- `POST /api/auth/register` → 201 (user created in PostgreSQL)
- `POST /api/auth/login` → 200 (returns JWT access + refresh tokens)
- `GET /` → 200 (React SPA served through Nginx)
- API proxy works: Nginx at :80 → Flask at :5000

---

## [2026-03-19] AI Service — Switched from Claude to Gemini

### Changes
- `backend/app/services/ai_service.py` — Replaced Anthropic SDK with `google-genai`, using `gemini-2.0-flash` model
- `backend/config.py` — `ANTHROPIC_API_KEY` → `GEMINI_API_KEY`
- `backend/requirements.txt` — `anthropic` → `google-genai`
- `docker-compose.yml` — Env var updated to `GEMINI_API_KEY`
- `.env` + `.env.example` — Updated to `GEMINI_API_KEY`

---

## [2026-03-19] Bug Fixes — JWT Identity & Marshmallow

### JWT Identity (str vs int)
- Flask-JWT-Extended v4.7 requires `identity` to be a string
- All `create_access_token(identity=user.id)` changed to `str(user.id)`
- Created `get_current_user_id()` helper in `utils/decorators.py` that does `int(get_jwt_identity())`
- Updated all route files (auth, challenges, ai, social) to use the helper
- **Root cause**: Login succeeded but all subsequent API calls returned 422 "Subject must be a string", causing redirect loop

### Marshmallow null fields
- `ChatInputSchema` — `conversation_id` and `challenge_id` now `allow_none=True, load_default=None`
- Fixes AI Coach failing on first message when these are null

---

## [2026-03-19] GitHub-Inspired Profile Page

### Backend Changes
- `backend/app/services/social_service.py` — Added `get_full_profile()` returning rich profile data: user info, profile, stats (challenges, streaks, followers), challenge cards, activity heatmap data, activity feed
- `backend/app/api/social/routes.py` — `/profile/<username>` now calls `get_full_profile()`

### Frontend Files Created
- `frontend/src/pages/Profile.jsx` — Main profile page with 3 tabs (Overview, Challenges, Activity), GitHub-style layout with sidebar + main content
- `frontend/src/components/social/ProfileSidebar.jsx` — Avatar (initials fallback), display name, username, bio, follow button, stats (days completed, challenges, streaks), join date
- `frontend/src/components/social/ChallengeCard.jsx` — Card with title, status badge, difficulty dot, day counter, progress bar (like GitHub repo cards)
- `frontend/src/components/social/ActivityHeatmap.jsx` — GitHub-style contribution heatmap (52 weeks, 7 rows), color-coded by task completion ratio, with month labels and legend
- `frontend/src/components/social/ActivityFeed.jsx` — Timeline with icons per activity type, date labels, day badges

### Routing & Navigation
- Added `/profile/:username` route in `App.jsx`
- Username in navbar now links to profile page

---

## [2026-03-19] Heatmap Redesign — 75-Day Challenge Grid

### Changes
- `frontend/src/components/social/ActivityHeatmap.jsx` — Complete rewrite
  - Changed from 52-week yearly view to **75-day challenge-specific grid** (11 columns x 7 rows)
  - Color scale: light green (`#39d353`) = all tasks completed, dark green (`#0e4429`) = 1 task completed
  - Shows `X of 75 days completed — Day N` header with challenge title badge
  - Week labels (W1, W2, W4...) above columns
  - Hover tooltip: `Day X: 3/5 tasks — completed`
  - Uses GitHub's exact green palette: `#161b22`, `#0e4429`, `#006d32`, `#26a641`, `#39d353`
  - Red tint for missed days
- `frontend/src/pages/Profile.jsx` — Passes `challenges` prop to heatmap

---

## [2026-03-19] Heatmap Layout Fix — Full-Width Spread

### Changes
- `frontend/src/components/social/ActivityHeatmap.jsx` — Fixed cramped grid
  - Changed from fixed-width `w-[13px]` cells to `flex-1 aspect-square` so cells stretch evenly across full container width
  - Week columns use `flex-1` for equal distribution
  - Added `gap-[3px]` between cells for clean spacing
  - Week labels also use `flex-1` and center-align above their column

---
