from time import sleep, time

import pruddb
from loguru import logger
from prud import discord, polyring
from prud.config import config

last_feed_sync = 0
last_post_sync = 0


def fetch_and_send_new_posts(
    db_connection: pruddb.PrudDbConnection,
    oldest_allowed_to_send: int = 0,
):
    new_posts = polyring.update_db_posts_and_get_new_posts(db_connection=db_connection)
    for post in new_posts:
        if post.published > oldest_allowed_to_send:
            logger.info(f"Sending new Post titled {post.title} dated {post.published}")
            post_as_webhook_body = discord.WebhookPostObject.from_post(
                post, db_connection=db_connection
            )
            discord.send_to_webhook(post_as_webhook_body)
        else:
            logger.info(
                f"Skipping newly found Post title {post.title} because its too old"
            )
        db_connection.handle_post(post)


if __name__ == "__main__":
    db_connection = pruddb.PrudDbConnection(db_url=config.db_url)
    while True:
        current_time = int(time())
        if current_time - last_feed_sync > config.feed_sync_interval_s:
            polyring.update_db_feeds(db_connection=db_connection)
            last_feed_sync = current_time
        if current_time - last_post_sync > config.post_sync_interval_s:
            fetch_and_send_new_posts(
                db_connection=db_connection,
                oldest_allowed_to_send=config.oldest_post_to_send_ts,
            )
            last_post_sync = current_time
        logger.info(f"Sleeping for {config.main_loop_interval_s} seconds :)")
        sleep(config.main_loop_interval_s)
