import utils.utils as utils
from lib.reddit import find_snapshot_post
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from lib.constants import *

# Setup scheduler
scheduler = BackgroundScheduler(timezone="UTC")

scheduler.add_job(find_snapshot_post, trigger=IntervalTrigger(
    start_date=utils.calculate_snapshot_date(),
    days=28
))
