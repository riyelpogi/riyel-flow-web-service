from datetime import date as Date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.dashboard import service
from app.dashboard.schemas.dashboard_response import DashboardResponse

router = APIRouter()


@router.get('/dashboard', response_model=DashboardResponse)
def fetch_dashboard(
    user_id: int = Query(gt=0),
    date: Date | None = Query(default=None, description='Dashboard date (YYYY-MM-DD)'),
    db: Session = Depends(get_db),
):
    return service.fetch_dashboard(db=db, user_id=user_id, date=date)
