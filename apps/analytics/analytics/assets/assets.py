from dagster import asset, get_dagster_logger

from analytics.extract.items import get_osrsbox_db
from models.items import OsrsItemDb

from analytics.processing.tick_count import (
    calculate_all_user_tick_counts,
    load_all_user_tick_counts,
)

from analytics.processing.equipment import (
    calculate_equipment_tick_counts_for_user,
    load_equipment_tick_counts_for_user,
)
from analytics.resources import MongoClient

_logger = get_dagster_logger(__name__)


@asset
def tick_count(
    mongo_client: MongoClient,
):
    tick_counts = calculate_all_user_tick_counts(
        raw_db_client=mongo_client.get_raw_client()
    )
    _logger.info(f"Calculated tick counts for {len(tick_counts)} users")

    load_all_user_tick_counts(
        tick_counts,
        analytics_db_client=mongo_client.get_analytics_client(),
    )
    _logger.info(f"Loaded tick counts for {len(tick_counts)} users")


@asset()
def osrs_item_db() -> OsrsItemDb:
    return get_osrsbox_db()


@asset()
def equipment_analysis(
    osrs_item_db: OsrsItemDb,
    mongo_client: MongoClient,
):
    """
    Counts the number of game ticks a player has spent wearing each piece of equipment.
    """

    raw_db_client = mongo_client.get_raw_client()
    analytics_db_client = mongo_client.get_analytics_client()

    # get all usernames
    # TODO(j.swannack): make into asset
    usernames = raw_db_client.get_game_tick_collection().distinct("username")

    for username in usernames:
        user_equipment_count = calculate_equipment_tick_counts_for_user(
            username=username,
            raw_db_client=raw_db_client,
            osrs_item_db=osrs_item_db,
        )
        load_equipment_tick_counts_for_user(
            user_equipment_count=user_equipment_count,
            analytics_db_client=analytics_db_client,
        )
