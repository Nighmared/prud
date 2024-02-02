from time import time
from typing import Optional

from loguru import logger
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field, Session, SQLModel, create_engine, desc, select

Base = declarative_base


BACKOFF_STEPS = 3600  # 1h


class PolyRingFeed(SQLModel, table=True):
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
    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(default=None, foreign_key=PolyRingFeed.id)
    title: str
    link: str
    guid: str
    summary: str
    published: int
    handled: bool = False


class PrudDbConnection:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def add_feed(self, feed: PolyRingFeed):
        with Session(self.engine) as session:
            session.add(feed)
            session.commit()

    def add_feeds(self, feeds: list[PolyRingFeed]):
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

    def handle_post(self, post: PolyRingPost):
        with Session(self.engine) as session:
            db_post = session.exec(
                select(PolyRingPost).where(PolyRingPost.id == post.id)
            ).one()
            db_post.handled = True
            session.commit()

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

    def disable_feed(self, feed: PolyRingFeed):
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
            db_feed.disabled_until = int(time()) + db_feed.backoff_level * BACKOFF_STEPS
            session.commit()
            logger.info(
                f"disabled {feed.url} for {db_feed.backoff_level*BACKOFF_STEPS} seconds"
            )

    def enable_feed(self, feed: PolyRingFeed):
        with Session(self.engine) as session:
            db_feed = session.exec(
                select(PolyRingFeed).where(PolyRingFeed.id == feed.id)
            ).one_or_none()
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
