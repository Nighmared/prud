from typing import Optional

import pruddb
from config import config
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
if config.env == "dev":
    origins = [
        "http://localhost:8802",
        "http://localhost:3000",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

router = APIRouter()


db_connection = pruddb.PrudDbConnection(config.db_url)


class PolyRingFeedData(BaseModel):
    id: int
    title: str
    url: str
    feed: str
    enabled: bool
    disabled_until: Optional[int]


class PolyRingPostData(BaseModel):
    title: str
    link: str
    summary: str
    published: int


class ReadPostsResponse(BaseModel):
    feed: PolyRingFeedData
    posts: list[PolyRingPostData]


class ReadFeedsResponse(BaseModel):
    feeds: list[PolyRingFeedData]


def data_post_from_db_post(db_post: pruddb.PolyRingPost) -> PolyRingPostData:
    return PolyRingPostData(
        title=db_post.title,
        link=db_post.link,
        summary=db_post.summary,
        published=db_post.published,
    )


def data_feed_from_db_feed(db_feed: pruddb.PolyRingFeed) -> PolyRingFeedData:
    return PolyRingFeedData(
        id=db_feed.id,
        title=db_feed.title,
        enabled=db_feed.enabled,
        feed=db_feed.feed,
        url=db_feed.url,
        disabled_until=db_feed.disabled_until,
    )


@router.get("/feeds")
def read_feeds():
    db_feeds = db_connection.get_feeds()
    data_feeds = [data_feed_from_db_feed(f) for f in db_feeds]
    response = ReadFeedsResponse(feeds=data_feeds)
    return response


@router.get("/feeds/{feed_id}")
def read_posts(feed_id: int):
    feed = db_connection.get_feed_from_id(feed_id)
    if feed is None:
        raise HTTPException(status_code=404, detail="Feed ID not found")
    db_posts = db_connection.get_posts_from_feed_id(feed_id)
    data_feed = data_feed_from_db_feed(feed)
    data_posts = [data_post_from_db_post(p) for p in db_posts]
    response = ReadPostsResponse(feed=data_feed, posts=data_posts)
    return response


@router.get("/status")
def status():
    return {"status": "okay"}

app.include_router(router, prefix="/api")
