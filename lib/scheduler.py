import pytz
import utils.utils as utils
from lib.reddit import find_snapshot_post
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Setup scheduler
scheduler = BackgroundScheduler(timezone="UTC")

start_date = utils.calculate_snapshot_date()
start_date = pytz.UTC.localize(start_date)

scheduler.add_job(find_snapshot_post, trigger=IntervalTrigger(
    start_date=start_date, 
    days=28
))
