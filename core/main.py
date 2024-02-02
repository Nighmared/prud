from time import sleep
from typing import Callable

import alembic.config
import pruddb
from loguru import logger
from prud.config import config
from prud.looputil import LoopManager

from prud import discord, feedutil, polyring


def fetch_and_send_new_posts(
    db_connection: pruddb.PrudDbConnection,
):
    """Central connector function that fetches new posts
    from the xml feeds, stores them in the db and sends them
    to the discord channel via webhook
    """
    new_posts = polyring.update_db_posts_and_get_new_posts(db_connection=db_connection)
    for post in new_posts:
        if post.published > config.oldest_post_to_send_ts:
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


loop_config: list[tuple[int, Callable[[pruddb.PrudDbConnection], None]]] = [
    (config.feed_sync_interval_s, polyring.update_db_feeds),
    (config.feed_reenable_interval_s, feedutil.iter_disabled_feeds_and_re_enable),
    (config.post_sync_interval_s, fetch_and_send_new_posts),
    (config.recover_backoff_interval_s, feedutil.recover_backoff_level),
]


def main():
    db_connection = pruddb.PrudDbConnection(db_url=config.db_url)

    # run migrations
    alembic_args: list[str] = []
    if config.alembic == "local":
        alembic_args.extend(["-n", "local"])
    alembic_args.extend(
        [
            "--raiseerr",
            "upgrade",
            "head",
        ]
    )
    logger.info("Applying DB Migrations")
    alembic.config.main(argv=alembic_args)

    loop_manager = LoopManager(db_connection=db_connection)
    loop_manager.import_config(loop_config)

    while True:
        loop_manager.check_all_loops()
        sleep(config.main_loop_interval_s)


if __name__ == "__main__":
    main()
