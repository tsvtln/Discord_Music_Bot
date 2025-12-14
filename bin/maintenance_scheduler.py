"""
Daily maintenance scheduler: wipes draw_data and reroll_data at 00:00.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


def _wipe_daily_tables():
    # Local import to avoid circular deps
    from bin.db_helpers import DBHelpers
    # Clear tables. Use TRUNCATE for full wipe; or DELETE for safety.
    try:
        DBHelpers.execute("TRUNCATE TABLE draw_data")
    except Exception:
        # Fallback to DELETE if TRUNCATE fails due to permissions
        DBHelpers.execute("DELETE FROM draw_data")
    try:
        DBHelpers.execute("TRUNCATE TABLE reroll_data")
    except Exception:
        DBHelpers.execute("DELETE FROM reroll_data")


_scheduler = None


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return _scheduler
    scheduler = AsyncIOScheduler(timezone="UTC")
    # Run daily at 00:00 local time. If you need a specific timezone, adjust timezone above.
    scheduler.add_job(_wipe_daily_tables, CronTrigger(hour=0, minute=0))
    scheduler.start()
    _scheduler = scheduler
    return scheduler

