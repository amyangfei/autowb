from apscheduler.scheduler import Scheduler

_scheduler = Scheduler()
# _scheduler = Scheduler(daemonic=False)
_scheduler.start()


def get_scheduler():
    return _scheduler
