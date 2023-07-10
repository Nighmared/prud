from typing import Optional

from sqlmodel import Field, SQLModel


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
