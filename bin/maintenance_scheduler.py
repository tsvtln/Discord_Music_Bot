"""
Daily maintenance scheduler: wipes draw_data and reroll_data at 00:00, and cleans cache.
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


def _clean_cache():
    """Clean cache files older than 24 hours"""
    from bin.cache_cleaner import CacheCleaner
    print("Running daily cache cleanup...")
    CacheCleaner.clean_cache(max_age_hours=24)


_scheduler = None


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return _scheduler
    scheduler = AsyncIOScheduler(timezone="UTC")
    # Run daily at 00:00 local time. If you need a specific timezone, adjust timezone above.
    scheduler.add_job(_wipe_daily_tables, CronTrigger(hour=0, minute=0))
    # Clean cache daily at 00:05
    scheduler.add_job(_clean_cache, CronTrigger(hour=0, minute=5))
    scheduler.start()
    _scheduler = scheduler
    return scheduler

