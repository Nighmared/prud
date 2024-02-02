import re
from html import unescape
from time import time

import feedparser
import loguru
import pruddb
import requests
from dateutil import parser as dateparser
from dateutil import tz
from feedparser.util import FeedParserDict
from prud.config import config

logger = loguru.logger

tzinfos = {"CET": tz.gettz("CET")}


def _raw_post_to_object(raw_post, feed_id) -> pruddb.PolyRingPost:
    try:
        summary = re.sub(r"<.*?>", "", raw_post.summary)
    except AttributeError:
        summary = ""
    link: str = raw_post.link
    if not link.startswith("http"):
        link = "http://" + link
    try:
        guid = raw_post.guid
    except AttributeError:
        guid = link
    # replace something like "&amp;" with the actual character which in that case would be "&"
    summary = unescape(summary)
    published = int(dateparser.parse(raw_post.published, tzinfos=tzinfos).timestamp())
    return pruddb.PolyRingPost(
        feed_id=feed_id,
        guid=guid,
        link=link,
        published=published,
        title=raw_post.title,
        summary=summary,
    )


def posts_from_feed(feed: pruddb.PolyRingFeed) -> list[pruddb.PolyRingPost]:
    try:
        response = requests.get(feed.feed, timeout=config.feed_request_timeout)
    except requests.exceptions.Timeout as exc:
        raise ConnectionError("Timed out") from exc
    except requests.exceptions.ConnectionError as exc:
        raise ConnectionError("ConnectionError") from exc
    parsed: FeedParserDict = feedparser.parse(response.content)
    raw_posts = parsed.entries
    posts = [_raw_post_to_object(p, feed.id) for p in raw_posts]
    return posts


def iter_disabled_feeds_and_re_enable(db_connection: pruddb.PrudDbConnection) -> None:
    now = int(time())
    feeds = db_connection.get_disabled_feeds()
    for feed in feeds:
        if feed.disabled_until is None:  # catchall for when this is a new feature
            logger.info(f"re enabling {feed.title}")
            db_connection.enable_feed(feed)
            return
        if feed.disabled_until < now:
            logger.info(f"re enabling {feed.title}")
            db_connection.enable_feed(feed)


def recover_backoff_level(db_connection: pruddb.PrudDbConnection) -> None:
    enabled_feeds = db_connection.get_feeds(only_enabled=True)
    for feed in enabled_feeds:
        db_connection.decrease_backoff_level(feed)
