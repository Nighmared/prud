import re
from html import unescape

import feedparser
import loguru
import requests
from dateutil import parser as dateparser

logger = loguru.logger

import pruddb
from prud.config import config


def _raw_post_to_object(raw_post, feed_id) -> pruddb.PolyRingPost:
    try:
        guid = raw_post.guid
    except AttributeError:
        guid = raw_post.link
    try:
        summary = re.sub(r"<.*?>", "", raw_post.summary)
    except AttributeError:
        summary = ""
    # replace something like "&amp;" with the actual character which in that case would be "&"
    summary = unescape(summary)
    published = int(dateparser.parse(raw_post.published).timestamp())
    link:str = raw_post.link
    if not link.startswith("http"):
        link = "http://"+link
    return pruddb.PolyRingPost(
        feed_id=feed_id,
        guid=guid,
        link=raw_post.link,
        published=published,
        title=raw_post.title,
        summary=summary,
    )


def posts_from_feed(feed: pruddb.PolyRingFeed) -> list[pruddb.PolyRingPost]:
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
