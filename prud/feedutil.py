import feedparser
import loguru
import requests

logger = loguru.logger

from prud import config, db


def _raw_post_to_object(raw_post, feed_id) -> db.Post:
    try:
        guid = raw_post.guid
    except AttributeError:
        guid = raw_post.link

    return db.Post(
        feed_id=feed_id,
        guid=guid,
        link=raw_post.link,
        published=raw_post.published,
        title=raw_post.title,
    )


def posts_from_feed(feed: db.PolyRingFeed) -> list[db.Post]:
    try:
        response = requests.get(feed.feed, timeout=config.feed_request_timeout)
    except requests.exceptions.Timeout:
        raise ConnectionError("Timed out")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("ConnectionError")
    parsed = feedparser.parse(response.content)
    raw_posts = parsed.entries
    posts = [_raw_post_to_object(p, feed.id) for p in raw_posts]
    return posts
