from dagster import asset, get_dagster_logger

from analytics.tick_count import calculate_all_user_tick_counts

logger = get_dagster_logger(__name__)


# TODO(j.swannack): resource for mongo client
@asset
def tick_count():
    return calculate_all_user_tick_counts()


@asset
def hey(tick_count: dict):
    logger.info("hey this is the pipeline running")
    logger.info("goodbye")
    logger.info(tick_count)
    print("hey")