import utils.utils as utils
from lib.scheduler import scheduler

# Start scheduler to update snapshot csv post data
scheduler.start()

from lib.reddit import reddit, get_latest_snapshot
from lib.constants import *
from lib.credentials import *
import lib.globals as glob
import time

get_latest_snapshot()

subreddit = reddit.subreddit("CryptoCurrency")

for comment in subreddit.stream.comments(skip_existing=True):

    try:
        # only process comments from other users
        if (comment.author != REDDIT_USERNAME):
            if (comment.submission.id == glob.snapshot_post_id):
                print("SNAPSHOT COMMENT !!!!")
            print(comment.author)
            # if ()
            time.sleep(1)

    except Exception as e:
       print(f"failed to process comment: {e}")
