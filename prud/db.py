from datetime import datetime
from typing import Optional

from loguru import logger
from sqlmodel import Field, Session, SQLModel, create_engine, select

from prud import config


class PolyRingFeed(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    url: str = Field(unique=True)
    feed: str = Field(unique=True)
    enabled: bool = True

    def __ne__(self, __value: object) -> bool:
        if type(__value) != PolyRingFeed:
            return True
        if __value.title != self.title:
            return True
        if __value.url != self.url:
            return True
        return False


class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    feed_id: int = Field(default=None, foreign_key=PolyRingFeed.id)
    title: str
    link: str
    guid: str
    published: Optional[datetime]


engine = create_engine(config.db_url)
SQLModel.metadata.create_all(engine)


def add_feed(feed: PolyRingFeed):
    with Session(engine) as session:
        session.add(feed)
        session.commit()


def add_feeds(feeds: list[PolyRingFeed]):
    with Session(engine) as session:
        session.add_all(feeds)
        session.commit()


def add_post(post: Post):
    with Session(engine) as session:
        session.add(
            post,
        )
        session.commit()


def add_posts(posts: list[Post]):
    with Session(engine) as session:
        session.add_all(posts)
        session.commit()


def get_posts_from_feed_id(feed_id: int) -> list[Post]:
    with Session(engine) as session:
        posts = session.exec(select(Post).where(Post.feed_id == feed_id)).all()
    return posts


def disable_feed(feed: PolyRingFeed):
    with Session(engine) as session:
        db_feed = session.exec(
            select(PolyRingFeed).where(PolyRingFeed.id == feed.id)
        ).one_or_none()
        if db_feed is None:
            logger.critical("Tried to disable non-existing feed")
            return
        db_feed.enabled = False
        session.commit()


def get_feeds() -> list[PolyRingFeed]:
    with Session(engine) as session:
        feeds = session.exec(select(PolyRingFeed).where(PolyRingFeed.enabled)).all()

    return feeds
