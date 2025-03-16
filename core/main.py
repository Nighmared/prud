from time import sleep
from typing import Callable, Sequence

import alembic.config
import pruddb
from loguru import logger
from prud.config import config
from prud.looputil import LoopManager
from pruddb.exceptions import UserNotFoundError

from prud import discord, feedutil, polyring


def fetch_and_send_new_posts(
    db_connection: pruddb.PrudDbConnection,
):
    """Central connector function that fetches new posts
    from the xml feeds, stores them in the db and sends them
    to the discord channel via webhook
    """
    new_posts = polyring.update_db_posts_and_get_new_posts(db_connection=db_connection)
    send_posts(new_posts, db_connection=db_connection)


def send_post(post: pruddb.PolyRingPost, db_connection: pruddb.PrudDbConnection):
    send_posts([post], db_connection)


def send_posts(
    posts: Sequence[pruddb.PolyRingPost], db_connection: pruddb.PrudDbConnection
):
    for post in posts:
        if post.published > config.oldest_post_to_send_ts:
            logger.info(f"Sending Post titled {post.title} dated {post.published}")
            post_as_webhook_body = discord.WebhookPostObject.from_post(
                post, db_connection=db_connection
            )
            try:
                discord.send_to_webhook(post_as_webhook_body)
                db_connection.tag_post_sent(post)
            except discord.PostException:
                logger.warning("Failed to send post to discord!")
                continue
        else:
            logger.info(f"Not sending Post titled {post.title} because its too old")
        db_connection.handle_post(post)


def send_unhandled_posts(db_connection: pruddb.PrudDbConnection):
    unhandled_posts = db_connection.get_unhandled_posts()
    send_posts(unhandled_posts, db_connection=db_connection)


loop_config: list[tuple[int, Callable[[pruddb.PrudDbConnection], None]]] = [
    (config.feed_sync_interval_s, polyring.update_db_feeds),
    (config.feed_reenable_interval_s, feedutil.iter_disabled_feeds_and_re_enable),
    (config.send_unhandled_posts_interval_s, send_unhandled_posts),
    (config.post_sync_interval_s, fetch_and_send_new_posts),
    (config.recover_backoff_interval_s, feedutil.recover_backoff_level),
]


def ensure_admin_acc(db_connection: pruddb.PrudDbConnection):
    if config.admin_username is None or config.admin_pw is None:
        logger.info("Not ensuring an admin account exist. No Credentials were set")
        return  # nothing to do
    else:
        logger.info(f"Admin Credentials received: [Username: {config.admin_username}]")
        try:
            existing_user = db_connection.get_user_from_username(config.admin_username)
            password_match = existing_user.verify(config.admin_pw)
            if password_match:
                logger.info("User already exists")
            else:
                logger.info(
                    "User already exists but with different password. Updating..."
                )
                db_connection.change_password(config.admin_username, config.admin_pw)
        except UserNotFoundError:
            logger.info("Creating new User")
            new_user = pruddb.User.from_plaintext_pw(
                username=config.admin_username,
                password=config.admin_pw,
                email="admin@local.org",
                role=pruddb.Role.ADMIN,
            )
            db_connection.add_user(new_user)


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

    ensure_admin_acc(db_connection)

    loop_manager = LoopManager(db_connection=db_connection)
    loop_manager.import_config(loop_config)

    while True:
        loop_manager.check_all_loops()
        sleep(config.main_loop_interval_s)


if __name__ == "__main__":
    main()
