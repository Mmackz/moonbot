import praw
import re
import time
import lib.globals as glob
import utils.utils as utils
from utils.file_handler import FileHandler
from lib.comments import *
from lib.constants import SUB_FULLNAME
from lib.credentials import *

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    password=REDDIT_PASSWORD,
    user_agent="MoonBot:v1.0 (by /u/Mcgillby)",
    username=REDDIT_USERNAME
)

subreddit = reddit.subreddit("CryptoCurrency")

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
        utils.set_globals()
        return True
    return False

def find_snapshot_post():
    """Searches for a snapshot post every 30 seconds until one is found, for a maximum of 8 hours."""
    user = reddit.redditor("communitypoints")
    latest_post_id = None
    for _ in range(960):
        posts = get_latest_posts(user)
        if posts[0].id != latest_post_id:
            latest_post_id = posts[0].id
            for post in posts:
                if is_valid_post(post) and utils.calculate_post_age(post) < 90:
                    if process_post(post):
                        try:
                            snapshot = post.reply(moon_stats(glob.total_karma, glob.total_moons, glob.karma_ratio))
                            snapshot.mod.distinguish(sticky=True)
                        except Exception as e:
                            print(f"An error occurred trying to sticky the moon data: {e}")
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
                # Check if first comment is stickied
                first_comment = next(iter(post.comments), None)
                # If no comments or stickied comment
                if not first_comment or not first_comment.stickied:
                    # Sticky Round Stats
                    try:
                        snapshot = post.reply(moon_stats(glob.total_karma, glob.total_moons, glob.karma_ratio))
                        snapshot.mod.distinguish(sticky=True)
                    except Exception as e:
                        print(f"An error occurred trying to sticky the moon data: {e}")
                return

def process_comment(comment):
    author = comment.author
    if (author != REDDIT_USERNAME):
        if (comment.submission.id == glob.snapshot_post_id):
            username = utils.parse_comment(comment.body, author)
            if username:
                csv_handler = FileHandler("data/snapshot.csv")
                csv = csv_handler.read_csv()
                found = False
                for row in csv:
                    if row[0].lower() == f"u/{username}".lower():
                        moons = round(int(row[3]) * glob.karma_ratio)
                        try:
                            comment.reply(body=info_reply(username, row[3], glob.karma_ratio, moons))
                        except Exception as e:
                            print(f"An error occurred when sending a reply: {e}")
                        found = True
                        break
                if not found:
                    try:
                        comment.reply(body=not_found(username))
                    except Exception as e:
                        print(f"An error occurred when sending a reply: {e}")
        print(author)
        time.sleep(0.5)