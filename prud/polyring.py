import loguru
import requests
from pydantic import parse_obj_as

from prud import db, feedutil
from prud.config import config

logger = loguru.logger


def get_online_feeds() -> list[db.PolyRingFeed]:
    response = requests.get(config.polyring_members_url)
    feeds = parse_obj_as(list[db.PolyRingFeed], response.json())
    return feeds


def update_db_feeds():
    online_feeds = get_online_feeds()
    db_feeds = db.get_feeds()

    feed_url_to_feed: dict[str, db.PolyRingFeed] = dict()
    for feed in db_feeds:
        feed_url_to_feed[feed.url] = feed
    feed = None

    new_feeds: list[db.PolyRingFeed] = []

    for feed in online_feeds:
        if feed_url_to_feed.get(feed.url) is None:
            logger.debug(f"Adding feed at {feed.url}")
            new_feeds.append(feed)
            continue
        if feed != feed_url_to_feed[feed.url]:
            logger.critical("implement updating existing feeds!")

    db.add_feeds(new_feeds)
    logger.info(f"Added {len(new_feeds)} new feeds")


def update_db_posts_and_get_new_posts() -> list[db.Post]:
    feeds = db.get_feeds(only_enabled=True)
    all_new_posts: list[db.Post] = []
    for feed in feeds:
        new_posts = _get_new_feed_posts(feed)
        db.add_posts(new_posts)
        all_new_posts += new_posts

    logger.info(f"Got {len(all_new_posts)} new posts")
    return all_new_posts


def _get_new_feed_posts(feed: db.PolyRingFeed) -> list[db.Post]:
    logger.info(f"Getting new Posts for blog at {feed.url}")
    try:
        online_posts = feedutil.posts_from_feed(feed)
    except ConnectionError:
        logger.critical(f"Had troubles getting to feed at {feed.url}")
        db.disable_feed(feed)
        return []
    db_posts = db.get_posts_from_feed_id(feed.id)

    guid_to_db_post: dict[str, db.Post] = dict()
    for post in db_posts:
        guid_to_db_post[post.guid] = post
    post = None

    new_posts: list[db.Post] = []
    for post in online_posts:
        if (
            guid_to_db_post.get(post.guid) is None
            or not guid_to_db_post[post.guid].handled
        ):
            new_posts.append(post)

    return new_posts
