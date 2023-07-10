from typing import Optional

from loguru import logger
from sqlmodel import Field, Session, SQLModel, create_engine, select


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

    def add_post(self, post: Post):
        with Session(self.engine) as session:
            session.add(
                post,
            )
            session.commit()

    def add_posts(self, posts: list[Post]):
        with Session(self.engine) as session:
            session.expire_on_commit = False
            session.add_all(posts)
            session.commit()

    def handle_post(self, post: Post):
        with Session(self.engine) as session:
            db_post = session.exec(select(Post).where(Post.id == post.id)).one()
            db_post.handled = True
            session.commit()

    def _yeet_posts(self):
        logger.critical("Yeeting all posts, MAKE SURE THIS IS NOT CALLED FOR PROD!!!")
        with Session(self.engine) as session:
            posts = session.exec(select(Post))
            for p in posts:
                session.delete(p)
            session.commit()

    def get_posts_from_feed_id(self, feed_id: int) -> list[Post]:
        with Session(self.engine) as session:
            posts = session.exec(select(Post).where(Post.feed_id == feed_id)).all()
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
            session.commit()

    def get_feeds(self, only_enabled=False) -> list[PolyRingFeed]:
        with Session(self.engine) as session:
            if only_enabled:
                feeds = session.exec(
                    select(PolyRingFeed).where(PolyRingFeed.enabled == True)
                ).all()
            else:
                feeds = session.exec(select(PolyRingFeed)).all()
            return feeds
