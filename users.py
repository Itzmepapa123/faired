import pymongo
import json
import schedule
import time
import asyncio
from datetime import datetime
import pytz
from bot import Bot  # Import the existing bot instance from bot.py

# Configuration
DB_URI = "mongodb+srv://Mehtadmphta33:Mehtab1234@cluster0.2kwcnnv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Itachi"
CHANNEL_ID = -1002174377932
IST = pytz.timezone('Asia/Kolkata')  # Define IST timezone

# MongoDB setup
dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
user_data = database['users']

def fetch_user_ids():
    try:
        user_docs = user_data.find()
        user_ids = [doc['_id'] for doc in user_docs]
        return user_ids
    except Exception as e:
        print(f"Error fetching user IDs: {e}")
        return []

def save_user_ids_to_json(user_ids):
    try:
        with open('Itachi.json', 'w') as f:
            json.dump(user_ids, f)
    except Exception as e:
        print(f"Error saving user IDs to JSON file: {e}")

async def send_user_ids_to_channel():
    user_ids = fetch_user_ids()
    save_user_ids_to_json(user_ids)

    try:
        async with bot:
            with open('Itachi.json', 'rb') as f:
                await bot.send_document(CHANNEL_ID, f)
        print("User IDs sent to channel successfully.")
    except Exception as e:
        print(f"Error sending file to channel: {e}")

def job():
    # Function to run the scheduled task
    asyncio.run(send_user_ids_to_channel())

def schedule_job():
    now = datetime.now(IST)
    schedule_time = now.replace(hour=18, minute=58, second=0, microsecond=0)
    if now > schedule_time:
        schedule_time = schedule_time + timedelta(days=1)
    delay = (schedule_time - now).total_seconds()
    print(f"Next run at {schedule_time} IST")

    # Schedule the job to run daily at 07:30 IST
    schedule.every().day.at("07:30").do(job)

if __name__ == "__main__":
    schedule_job()
    while True:
        schedule.run_pending()
        time.sleep(60)  # Wait a minute before checking the schedule again
