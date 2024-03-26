import asyncio
from telegram import Bot
from telegram.error import TelegramError
import logging
from datetime import date,datetime
from time import sleep
import httpx
from telegram.ext import Updater
import constants
import os


daily_report = None
weekly_report = None
monthly_report = None
# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot API token
TOKEN = 'Your Token'

# List of chat IDs where you want to send messages

CHAT_IDS = [] # Add the users you want to send the report to 

# Read the file that contains the daily report

if os.path.exists(constants.daily_report_file_path):
    with open(constants.daily_report_file_path, "r", encoding="utf-8") as file:
        daily_report = file.read()
else:
    print("No file found.")

if os.path.exists(constants.weekly_report_file_path):
    with open(constants.weekly_report_file_path, "r", encoding="utf-8") as file:
        weekly_report = file.read()
else:
    print("No file found.")
    
if os.path.exists(constants.monthly_report_file_path):
    with open(constants.monthly_report_file_path, "r", encoding="utf-8") as file:
        monthly_report = file.read()
else:
    print("No file found.")


async def send_message_with_delay(bot, chat_id, text, delay):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Message sent to chat {chat_id}")
        await asyncio.sleep(delay)  # Wait for the specified delay
    except TelegramError as e:
        logger.error(f"Failed to send message to chat {chat_id}: {e}")

async def send_file_with_delay(bot, chat_id, file_path, delay):
    try:
        if os.path.exists(file_path):
            await bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))
            logger.info(f"File sent to chat {chat_id}")
        else:
            logger.info(f"No file found at {file_path}")
            print("No file found.")
        await asyncio.sleep(delay)  # Wait for the specified delay
    except TelegramError as e:
        logger.error(f"Failed to send file to chat {chat_id}: {e}")

async def main():
    bot = Bot(TOKEN)
    for chat_id in CHAT_IDS:
        await send_message_with_delay(bot, chat_id, "Hello Dear, I hope you're having a nice day <3\nHere are the Data", delay=5)
        if (daily_report):
            await send_message_with_delay(bot, chat_id, daily_report, delay=5)
        if (weekly_report):
            await send_message_with_delay(bot, chat_id, weekly_report, delay=5)
        if (monthly_report):
            await send_message_with_delay(bot, chat_id, monthly_report, delay=5)
        await send_file_with_delay(bot, chat_id, constants.daily_plots_path, delay=5)  # Send the Plot with today's date 
        await send_file_with_delay(bot, chat_id, constants.weekly_plots_path, delay=5)  # Send the Plot with today's date 
        await send_file_with_delay(bot, chat_id, constants.monthly_plots_path, delay=5)  # Send the Plot with today's date 
        await send_file_with_delay(bot, chat_id, constants.excel_file_path, delay=5)  # Send Excel file
        await send_message_with_delay(bot, chat_id, "With best wishes, Gold price seeker 2.0", delay=5)

if __name__ == '__main__':
    asyncio.run(main())
