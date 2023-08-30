import re
import requests
import logging
import lib.globals as glob
from datetime import datetime, timedelta
from lib.constants import START_SNAPSHOT_DATE, START_SNAPSHOT_ROUND
from utils.file_handler import FileHandler

def calculate_snapshot_date():
    now = datetime.utcnow()
    snapshot_date = datetime.fromisoformat(START_SNAPSHOT_DATE)
    while now >= snapshot_date:  
        snapshot_date += timedelta(days=28)
    return snapshot_date

def calculate_round_number():
    now = datetime.utcnow()
    start_date = datetime.fromisoformat(START_SNAPSHOT_DATE)
    elapsed_time = now - start_date
    elapsed_rounds = elapsed_time // timedelta(days=28) 
    return START_SNAPSHOT_ROUND + elapsed_rounds

def calculate_post_age(post):
    now = datetime.now().timestamp()
    created = post.created_utc  
    return now - created

def calculate_moon_data():
    # Calculate total moons for the round
    MOONS_PER_ROUND = 2_500_000
    round_number = calculate_round_number()
    total_moons_this_round = MOONS_PER_ROUND * (0.975 ** (round_number - 1))
    
    # Calculate total karma from the CSV
    total_karma = 0
    csv_handler = FileHandler("data/snapshot.csv")
    csv = csv_handler.read_csv()
    for row in csv[1:]:
        total_karma += int(row[3])

    # Check for division by zero
    if total_karma == 0:
        ratio = 0
    else:
        ratio = total_moons_this_round / total_karma
    
    return {
        "total_moons": total_moons_this_round,
        "total_karma": total_karma,
        "ratio": ratio
    }

def download_csv(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request failed
        if response.status_code == 200:
            csv_handler = FileHandler("data/snapshot.csv")
            if csv_handler.save_file(response.content):
                logging.info(f"CSV saved to {csv_handler.filepath}")
            else:
                logging.error("Failed to save CSV file")
                raise Exception("Failed to save CSV file")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while downloading the CSV: {e}")
        raise

def parse_comment(comment, author):    
    comment = comment.strip()

    # If comment is exactly "!lookup"
    if comment == "!lookup":
        return author

    # If comment matches the pattern "!lookup u/username" or "!lookup username"
    match = re.match(r'!lookup\s+(?:u/)?([\w-]{3,20})', comment)
    if match:
        return match.group(1)
    
    return None

def set_globals():
    data = calculate_moon_data()
    glob.karma_ratio = data["ratio"]
    glob.total_karma = data["total_karma"]
    glob.total_moons = data["total_moons"]