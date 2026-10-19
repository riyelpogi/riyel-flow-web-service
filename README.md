# Riyel Flow Web Service

FastAPI backend for the RiyelFlow application. Provides account registration and login, habits and completion logs, tasks, and a combined dashboard.

## Requirements

- Python 3.11 (the version used for local development)
- MySQL 8 and an initialized RiyelFlow database

## Local setup

Run the following commands from the project root.

### 1. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

If `.venv` already exists, only run the activation command. On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure the database

Create a local `.env` file in the project root:

```dotenv
DATABASE_URL=mysql+pymysql://YOUR_USER:YOUR_PASSWORD@localhost:3306/riyel_flow
```

Replace the placeholders with your MySQL credentials. URL-encode special characters in credentials. `.env` is ignored by Git and must be configured separately on each machine.

Create the database if it does not exist:

```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS riyel_flow;"
```

If you have a database dump, restore it using its actual path:

```bash
mysql -u root -p riyel_flow < /path/to/riyel_flow.sql
```

A SQL dump is not currently included in this repository. The application expects the `users`, `habits`, `habit_logs`, and `tasks` tables to exist; startup does not create tables or run migrations.

### 4. Start the service

```bash
python -m uvicorn app.main:app --reload
```

- Service: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

The root endpoint returns:

```json
{"message": "Riyel Flow Web Service Running"}
```

Press **Ctrl+C** to stop the server. Run `deactivate` to leave the virtual environment.

## API endpoints

Use `/riyel-flow` as the API base path. Request and response schemas are available in `/docs`.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/riyel-flow/auth/register-account` | Register an account |
| POST | `/riyel-flow/auth/login` | Log in and receive an access token |
| GET | `/riyel-flow/habits?user_id=5` | List a user's habits and completion flags |
| POST | `/riyel-flow/habits` | Create a habit |
| GET | `/riyel-flow/habit-logs?user_id=5` | List completion logs; optionally add `habit_id` |
| POST | `/riyel-flow/habit-logs` | Record a habit completion |
| GET | `/riyel-flow/tasks?user_id=5` | List a user's tasks |
| POST | `/riyel-flow/tasks` | Create a task |
| PATCH | `/riyel-flow/tasks/{task_id}/status` | Update task status |
| GET | `/riyel-flow/dashboard?user_id=5&date=2026-10-19` | Get progress and outstanding items for a date |

Habit frequencies are `daily`, `weekly`, and `monthly`. Task priorities are `low`, `medium`, and `high`; task statuses are `pending`, `in_progress`, and `completed`.

For example, update a task's status with:

```bash
curl -X PATCH http://localhost:8000/riyel-flow/tasks/3/status \
  -H 'Content-Type: application/json' \
  -d '{"status":"completed"}'
```

## Dashboard behavior

The optional `date` query parameter uses `YYYY-MM-DD` and defaults to today in `Asia/Manila`.

- `today_progress` includes totals, completed counts, and the combined completion percentage.
- `tasks` includes unfinished tasks due on or before the selected date, plus tasks without a due date.
- `habits` includes active habits with no completion in the selected day, Monday-based week, or calendar month, according to frequency.

Database timestamps are assumed to use Manila local time. Historical dashboards use current task status and current habit settings; they do not reconstruct past state. Weekly and monthly habit completion checks cover the whole selected period.

## Project structure

```text
app/
  main.py          # Application and router registration
  auth/            # Registration and login
  core/            # Database and security helpers
  dashboard/       # Combined dashboard
  habit_logs/      # Habit completion records
  habits/          # Habit definitions
  tasks/           # Task creation, listing, and status updates
  user/            # User model and queries
  utils/           # Shared date-period calculations
```

## Troubleshooting

- **Database connection failure:** check that MySQL is running, `DATABASE_URL` is correct, and the configured user can access the database.
- **Missing table:** initialize the database schema or restore a compatible SQL dump.
- **Import errors:** activate `.venv`, install requirements, and start Uvicorn from the project root.
- **404 response:** verify the `/riyel-flow` prefix and the HTTP method in `/docs`.

## Current access behavior

Login issues tokens, but the habits, habit logs, tasks, and dashboard routes currently do not enforce token authentication or ownership checks. JWT signing also uses a hardcoded fallback secret. These require changes before exposing the service publicly.
