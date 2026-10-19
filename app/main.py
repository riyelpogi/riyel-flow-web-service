from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.habits.router import router as habits_router
from app.habit_logs.router import router as habit_logs_router
from app.tasks.router import router as tasks_router
from app.dashboard.router import router as dashboard_router

app = FastAPI(
    title="Riyel Flow Web Service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Riyel Flow Web Service Running"}

app.include_router(auth_router, prefix="/riyel-flow/auth", tags=["Auth"])
app.include_router(habits_router, prefix="/riyel-flow", tags=["Habits"])
app.include_router(habit_logs_router, prefix="/riyel-flow", tags=["Habit Logs"])
app.include_router(tasks_router, prefix="/riyel-flow", tags=["Tasks"])
app.include_router(dashboard_router, prefix="/riyel-flow", tags=["Dashboard"])
