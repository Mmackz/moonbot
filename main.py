import logging
import utils.utils as utils
from lib.scheduler import scheduler
from lib.reddit import subreddit, get_latest_snapshot, process_comment

def main():
    # Start scheduler to update snapshot csv post data
    logging.info("Starting scheduler")
    scheduler.start()
    
    # Get latest snapshot
    get_latest_snapshot()

    for comment in subreddit.stream.comments(skip_existing=True):
        try:
            process_comment(comment)
        except Exception as e:
            logging.error(f"Failed to process comment: {e}", exc_info=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger("apscheduler").setLevel(logging.DEBUG)
    main()
