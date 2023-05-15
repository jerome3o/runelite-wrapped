import os
import time

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

URI = os.environ["MONGO_URI"]

client = MongoClient(URI)
db_raw = client.get_database("runelite-wrapped-raw")
db_analytics = client.get_database("runelite-wrapped-analytics")
game_tick_collection = db_raw.get_collection("game_ticks")
total_tick_collection = db_analytics.get_collection("tick_count")


def pull_game_tick_data(username: str):
    # Pull all game tick data for a certain player (username) and Calculate / count the number of gameticks
    game_tick_count = game_tick_collection.count_documents({"username": username})

    # Push that to the analytics collection (analytics.total_ticks)
    output = {
        "timestamp": time.time(),
        "value": game_tick_count,
        "username": username,
    }

    total_tick_collection.insert_one(output)


def main():
    pull_game_tick_data("jerome-o")


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()