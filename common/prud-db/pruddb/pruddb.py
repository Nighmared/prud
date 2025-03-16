"""Module to handle all communication between
the prud services and the db"""

from enum import Enum, auto
from time import time
from typing import Optional, Sequence

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from loguru import logger
from pruddb.exceptions import UserNotFoundError
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Field, Session, SQLModel, create_engine, desc, select

Base = declarative_base
ph = PasswordHasher()


FALLBACK_BACKOFF_STEPS = 3600  # 1h


class Role(Enum):
    DEFAULT = auto()
    ADMIN = auto()


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
    feed_id: int = Field(default=None, foreign_key="polyringfeed.id")
    title: str
    link: str
    guid: str
    summary: str
    published: int
    handled: bool = False
    sent: Optional[bool] = False


class User(SQLModel, table=True):
    """DB table to store users"""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str
    argon2_hash: str
    role: Role = Field(default=Role.DEFAULT, nullable=False)

    @staticmethod
    def from_plaintext_pw(
        username: str, password: str, email: str, role: Role = Role.DEFAULT
    ) -> "User":
        argon2_hash = ph.hash(password)
        new_user = User(
            username=username, email=email, argon2_hash=argon2_hash, role=role
        )
        return new_user

    def verify(self, password: str) -> bool:
        try:
            pass_match = ph.verify(self.argon2_hash, password)
        except VerificationError:
            return False
        return pass_match

    def update_password(self, password: str):
        self.argon2_hash = ph.hash(password)


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

    def add_user(self, user: User):
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def get_user_from_username(self, username: str) -> User:
        with Session(self.engine) as session:
            user = session.exec(
                select(User).where(User.username == username)
            ).one_or_none()
            if user is None:
                logger.debug("Tried to get user for unknown username")
                raise UserNotFoundError("Unknown User")
            return user

    def remove_user(self, user: User):
        with Session(self.engine) as session:
            session.delete(user)
            session.commit()

    def change_password(self, username: str, new_password: str):
        with Session(self.engine) as session:
            user = session.exec(
                select(User).where(User.username == username)
            ).one_or_none()
            if user is None:
                logger.debug("Tried to change pw for unknown username")
                raise UserNotFoundError("Unknown User")
            user.update_password(new_password)
            session.add(user)
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

    def delete_post(self, post: PolyRingPost):
        with Session(self.engine) as session:
            session.delete(post)
            session.commit()

    def get_post_from_id(self, post_id: int) -> PolyRingPost:
        with Session(self.engine) as session:
            post = session.exec(
                select(PolyRingPost).where(PolyRingPost.id == post_id)
            ).one_or_none()

            if post is None:
                logger.critical(f"Post for id {post_id} not found.")
                raise ValueError("invalid post id")
            return post

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

    def get_unhandled_posts(self) -> Sequence[PolyRingPost]:
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

    def get_posts_from_feed_id(self, feed_id: int) -> Sequence[PolyRingPost]:
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

    def get_feeds(self, only_enabled=False) -> Sequence[PolyRingFeed]:
        with Session(self.engine) as session:
            if only_enabled:
                feeds = session.exec(
                    select(PolyRingFeed).where(PolyRingFeed.enabled)
                ).all()
            else:
                feeds = session.exec(select(PolyRingFeed)).all()
            return feeds

    def get_disabled_feeds(self) -> Sequence[PolyRingFeed]:
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
