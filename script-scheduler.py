import schedule
import time as tm
import subprocess
import logging
import constants

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("Running GoldTracker")
        # Run periodic reports handler.py
        subprocess.run(['python', constants.main])
    except Exception as e:
        logger.error(f"An error occurred in main(): {e}")

# Schedule the main function to run every day at 2:30 PM
schedule.every().day.at("14:30").do(main)
schedule.every().day.at("20:00").do(main)

# Run pending scheduled tasks continuously
while True:
    schedule.run_pending()
    tm.sleep(60)