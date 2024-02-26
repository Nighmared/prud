import loguru
import pruddb
import requests
from prud.config import config
from pydantic import parse_obj_as

from prud import feedutil

logger = loguru.logger


def get_online_feeds() -> list[pruddb.PolyRingFeed]:
    try:
        response = requests.get(config.polyring_members_url, timeout=10)
    except TimeoutError as exc:
        raise ValueError("Couldn't reach polyring website within timeout") from exc
    feeds = parse_obj_as(list[pruddb.PolyRingFeed], response.json())
    return feeds


def update_db_feeds(db_connection: pruddb.PrudDbConnection):
    online_feeds = get_online_feeds()
    db_feeds = db_connection.get_feeds()

    feed_url_to_feed: dict[str, pruddb.PolyRingFeed] = {}
    for feed in db_feeds:
        feed_url_to_feed[feed.url] = feed
    feed = None

    new_feeds: list[pruddb.PolyRingFeed] = []

    for feed in online_feeds:
        if feed_url_to_feed.get(feed.url) is None:
            logger.debug(f"Adding feed at {feed.url}")
            new_feeds.append(feed)
            continue
        db_feed = feed_url_to_feed[feed.url]
        if db_feed != feed:
            db_connection.update_feed(db_feed, feed)

    db_connection.add_feeds(new_feeds)
    logger.info(f"Added {len(new_feeds)} new feeds")


def update_db_posts_and_get_new_posts(
    db_connection: pruddb.PrudDbConnection,
) -> list[pruddb.PolyRingPost]:
    feeds = db_connection.get_feeds(only_enabled=True)
    all_new_posts: list[pruddb.PolyRingPost] = []
    for feed in feeds:
        new_posts = _get_new_feed_posts(feed, db_connection=db_connection)
        db_connection.add_posts(new_posts)
        all_new_posts += new_posts

    logger.info(f"Got {len(all_new_posts)} new posts")
    return all_new_posts


def _get_new_feed_posts(
    feed: pruddb.PolyRingFeed, db_connection: pruddb.PrudDbConnection
) -> list[pruddb.PolyRingPost]:
    try:
        online_posts = feedutil.posts_from_feed(feed)
    except ConnectionError:
        logger.critical(f"Had troubles getting to feed at {feed.url}")
        db_connection.disable_feed(
            feed, backoff_steps=config.feed_disable_backoff_step_s
        )
        return []

    db_posts = db_connection.get_posts_from_feed_id(feed.id)

    guid_to_db_post: dict[str, pruddb.PolyRingPost] = dict()
    for post in db_posts:
        guid_to_db_post[post.guid] = post
    post = None

    new_posts: list[pruddb.PolyRingPost] = []
    for post in online_posts:
        if guid_to_db_post.get(post.guid) is None:
            new_posts.append(post)

    return new_posts
