import utils.utils as utils
from lib.scheduler import scheduler
from lib.reddit import subreddit, get_latest_snapshot, process_comment

# Start scheduler to update snapshot csv post data
scheduler.start()

# Get latest snapshot
get_latest_snapshot()

for comment in subreddit.stream.comments(skip_existing=True):
    try:
        process_comment(comment)
    except Exception as e:
        print(f"failed to process comment: {e}")
