"""Module to handle all communication between
the prud services and the db"""

from time import time
from typing import Optional

from loguru import logger
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field, Session, SQLModel, create_engine, desc, select

Base = declarative_base


FALLBACK_BACKOFF_STEPS = 3600  # 1h


class PolyRingFeed(SQLModel, table=True):
    """DB table for the different feeds"""

    id: int = Field(default=None, primary_key=True)
    title: str
    url: str = Field(unique=True)
    feed: str = Field(unique=True)
    enabled: bool = True
    backoff_level: Optional[int] = 0
    disabled_until: Optional[int] = 0

    def __ne__(self, __value: object) -> bool:
        if not isinstance(__value, PolyRingFeed):
            return True
        if __value.title != self.title:
            return True
        if __value.url != self.url:
            return True
        if __value.feed != self.feed:
            return True
        return False


class PolyRingPost(SQLModel, table=True):
    """DB Table to store blog posts"""

    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(default=None, foreign_key=PolyRingFeed.id)
    title: str
    link: str
    guid: str
    summary: str
    published: int
    handled: bool = False
    sent: Optional[bool] = False


class PrudDbConnection:
    """The class that provides methods for all
    required interactions with the db"""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_feed(self, feed: PolyRingFeed):
        """ "add feed to the db"""
        with Session(self.engine) as session:
            session.add(feed)
            session.commit()

    def add_feeds(self, feeds: list[PolyRingFeed]):
        """Add multiple feeds to the db in a batch"""
        with Session(self.engine) as session:
            session.add_all(feeds)
            session.commit()

    def get_feed_from_id(self, feed_id: int) -> PolyRingFeed:
        with Session(self.engine) as session:
            feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == feed_id)
            ).one_or_none()
            if feed is None:
                logger.critical("Feed for post not found, where did the id come from?")
                raise ValueError("Invalid feed id")
            return feed

    def add_post(self, post: PolyRingPost):
        with Session(self.engine) as session:
            session.add(
                post,
            )
            session.commit()

    def add_posts(self, posts: list[PolyRingPost]):
        with Session(self.engine) as session:
            session.expire_on_commit = False
            session.add_all(posts)
            session.commit()

    def tag_post_sent(self, post: PolyRingPost):
        with Session(self.engine) as session:
            db_post = session.exec(
                select(PolyRingPost).where(PolyRingPost.id == post.id)
            ).one()
            db_post.sent = True
            session.commit()

    def handle_post(self, post: PolyRingPost):
        with Session(self.engine) as session:
            db_post = session.exec(
                select(PolyRingPost).where(PolyRingPost.id == post.id)
            ).one()
            db_post.handled = True
            session.commit()

    def get_unhandled_posts(self) -> list[PolyRingPost]:
        with Session(self.engine) as session:
            posts = session.exec(
                select(PolyRingPost)
                .where(PolyRingPost.handled == 0)
                .order_by(desc(PolyRingPost.published))
            ).all()
            return posts

    def _yeet_posts(self):
        logger.critical("Yeeting all posts, MAKE SURE THIS IS NOT CALLED FOR PROD!!!")
        with Session(self.engine) as session:
            posts = session.exec(select(PolyRingPost))
            for p in posts:
                session.delete(p)
            session.commit()

    def get_posts_from_feed_id(self, feed_id: int) -> list[PolyRingPost]:
        with Session(self.engine) as session:
            posts = session.exec(
                select(PolyRingPost)
                .where(PolyRingPost.feed_id == feed_id)
                .order_by(desc(PolyRingPost.published))
            ).all()
            return posts

    def disable_feed(
        self, feed: PolyRingFeed, backoff_steps: int = FALLBACK_BACKOFF_STEPS
    ):
        with Session(self.engine) as session:
            db_feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == feed.id)
            ).one_or_none()
            if db_feed is None:
                logger.critical("Tried to disable non-existing feed")
                return
            db_feed.enabled = False
            current_backoff_level = db_feed.backoff_level or 0
            db_feed.backoff_level = min(72, current_backoff_level + 1)
            db_feed.disabled_until = int(time()) + db_feed.backoff_level * backoff_steps
            session.commit()
            logger.info(
                f"disabled {feed.url} for {db_feed.backoff_level*backoff_steps} seconds"
            )

    def enable_feed(self, feed: PolyRingFeed):
        with Session(self.engine) as session:
            db_feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == feed.id)
            ).one_or_none()
            if db_feed is None:
                logger.critical("Tried to enable non-existing feed")
                return
            db_feed.enabled = True
            session.commit()

    def update_feed(self, existing_feed: PolyRingFeed, changed_feed: PolyRingFeed):
        logger.info(f'Updating feed "{existing_feed.title}"')
        with Session(self.engine) as session:
            fresh_db_feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == existing_feed.id)
            ).one_or_none()
            if fresh_db_feed is None:
                logger.critical("Tried to update non-existing feed?")
                return
            if existing_feed.feed != changed_feed.feed:
                fresh_db_feed.feed = changed_feed.feed
            if existing_feed.title != changed_feed.title:
                fresh_db_feed.title = changed_feed.title
            session.commit()

    def get_feeds(self, only_enabled=False) -> list[PolyRingFeed]:
        with Session(self.engine) as session:
            if only_enabled:
                feeds = session.exec(
                    select(PolyRingFeed).where(PolyRingFeed.enabled)
                ).all()
            else:
                feeds = session.exec(select(PolyRingFeed)).all()
            return feeds

    def get_disabled_feeds(self) -> list[PolyRingFeed]:
        with Session(self.engine) as session:
            feeds = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.enabled == 0)
            ).all()
        return feeds

    def decrease_backoff_level(self, feed: PolyRingFeed, decrease_by=1) -> None:
        with Session(self.engine) as session:
            db_feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == feed.id)
            ).one_or_none()
            if db_feed is None:
                logger.critical("Tried to modify backoff of non-existing feed")
                return
            current_backoff_level = db_feed.backoff_level or 0
            db_feed.backoff_level = max(0, current_backoff_level - decrease_by)
            session.commit()
