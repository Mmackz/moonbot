import requests
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

def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        csv_handler = FileHandler("data/snapshot.csv")
        csv_handler.save_file(response.content)
        print(f"CSV saved to {csv_handler.filepath}")
    else:
        print(f"Failed to download CSV")