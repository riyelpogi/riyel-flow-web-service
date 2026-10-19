from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_periods(day=None):
    today = day if day is not None else datetime.now(ZoneInfo('Asia/Manila')).date()
    start = datetime.combine(today, datetime.min.time())
    week_start = start - timedelta(days=start.weekday())
    month_start = start.replace(day=1)
    next_month = (month_start + timedelta(days=32)).replace(day=1)
    return {
        'daily': (start, start + timedelta(days=1)),
        'weekly': (week_start, week_start + timedelta(days=7)),
        'monthly': (month_start, next_month),
    }
