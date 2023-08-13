import praw
import re
import time
import lib.globals as glob
import utils.utils as utils
from lib.constants import SUB_FULLNAME
from lib.credentials import *

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent="MoonBot:v1.0 (by /u/Mcgillby)",
    username=REDDIT_USERNAME
)

def is_snapshot_post(title):
    pattern = r'New Moons Distribution \(Round \d+ Proposal\)'
    return bool(re.match(pattern, title))

def extract_csv_url(post_text):
    pattern = r'https://reddit-meta-production\.s3\.amazonaws\.com/distribution/publish/CryptoCurrency/round_(\d+)_proposed\.csv'
    match = re.search(pattern, post_text)
    if match:
        return match.group(0)
    return None
        
def get_latest_posts(user, limit=2):
    return list(user.submissions.new(limit=limit))

def is_valid_post(post):
    return post.subreddit_id == SUB_FULLNAME and is_snapshot_post(post.title)

def process_post(post):
    url = extract_csv_url(post.selftext)
    if url:
        glob.snapshot_post_id = post.id
        utils.download_csv(url)
        return True
    return False

def find_snapshot_post():
    """Searches for a snpshot post every 30 seconds until one is found for a maximum of 8 hours."""
    user = reddit.redditor("communitypoints")
    latest_post_id = None
    for _ in range(960):
        posts = get_latest_posts(user)
        if posts[0].id != latest_post_id:
            latest_post_id = posts[0].id
            for post in posts:
                if is_valid_post(post) and utils.calculate_post_age(post) < 90:
                    if process_post(post):
                        return
        time.sleep(30)
    # Message bot maintainer if no csv post is found within the time limit
    reddit.redditor("mcgillby").message("No Snapshot Post Found", 
                                        "Please restart the bot once you have manually confirmed the new post is available")

def get_latest_snapshot():
    user = reddit.redditor("communitypoints")
    posts = get_latest_posts(user, limit=4)
    for post in posts:
        if is_valid_post(post):
            if process_post(post):
                return
