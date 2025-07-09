import datetime as dt
from typing import Annotated, Literal, Optional

import jwt
import pruddb
from config import config
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from loguru import logger
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


def check_auth(token: str, min_role: pruddb.Role):
    token_dec = jwt.decode(token, config.jwt_secret, algorithms=["HS256"])
    token_role = token_dec["role"]
    expires = dt.datetime.strptime(token_dec["expires"], "%a, %d %b %Y %H:%M:%S UTC")
    if expires < dt.datetime.now():
        # token has expired
        return False
    return pruddb.Role[token_role].value >= min_role.value


def is_admin(token: str) -> bool:
    return check_auth(token, pruddb.Role.ADMIN)


def is_root(token: str) -> bool:
    return check_auth(token, pruddb.Role.ROOT)


class PolyRingFeedData(BaseModel):
    id: int
    title: str
    url: str
    feed: str
    enabled: bool
    disabled_until: Optional[int]


class PolyRingPostData(BaseModel):
    id: int
    title: str
    link: str
    summary: str
    published: int


class UserCreateRequest(BaseModel):
    username: str
    password: str
    email: str
    role: Literal["DEFAULT", "ADMIN"] = "DEFAULT"


class ReadPostsResponse(BaseModel):
    feed: PolyRingFeedData
    posts: list[PolyRingPostData]


class ReadFeedsResponse(BaseModel):
    feeds: list[PolyRingFeedData]


def data_post_from_db_post(db_post: pruddb.PolyRingPost) -> PolyRingPostData:
    assert db_post.id is not None
    return PolyRingPostData(
        id=db_post.id,
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
    response_data = ReadFeedsResponse(feeds=data_feeds)
    return response_data


@router.get("/feeds/{feed_id}")
def read_posts(feed_id: int):
    try:
        feed = db_connection.get_feed_from_id(feed_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Feed ID not found") from exc
    db_posts = db_connection.get_posts_from_feed_id(feed_id)
    data_feed = data_feed_from_db_feed(feed)
    data_posts = [data_post_from_db_post(p) for p in db_posts]
    response_data = ReadPostsResponse(feed=data_feed, posts=data_posts)
    return response_data


@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response,
):
    username = form_data.username
    passw = form_data.password
    try:
        user = db_connection.get_user_from_username(username)
    except ValueError:
        response.status_code = 401
        return {"error": "Bad Login"}
    pass_match = user.verify(passw)
    if not pass_match:
        response.status_code = 401
        return {"error": "Bad Login"}

    expiry = dt.datetime.now(tz=dt.timezone.utc) + dt.timedelta(days=2)
    expiry_cookie = expiry.strftime("%a, %d %b %Y %H:%M:%S UTC")
    token_dict = {
        "username": user.username,
        "email": user.email,
        "role": user.role.name,
        "expires": str(expiry_cookie),
    }

    token = jwt.encode(token_dict, config.jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "expiry": str(expiry)}


@router.post("/user/create", status_code=201)
def create_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    user_data: UserCreateRequest,
):
    if is_root(token):
        new_user = pruddb.User.from_plaintext_pw(
            username=user_data.username,
            password=user_data.password,
            email=user_data.email,
            role=pruddb.Role[user_data.role],
        )
        db_connection.add_user(new_user)
    else:
        response.status_code = 401


@router.delete("/posts/{post_id}", status_code=204)
def deletePost(
    token: Annotated[str, Depends(oauth2_scheme)], response: Response, post_id: int
):
    response.status_code = 204
    if is_admin(token):
        try:
            post = db_connection.get_post_from_id(post_id)
            db_connection.delete_post(post)
        except ValueError:
            logger.warning("Authenticated user tried to delete non-existing post")
            response.status_code = 404
            return {"info": "Post ID not found"}
    else:
        response.status_code = 401
        return {"info": "Not an Admin"}


@router.delete("/feeds/{feed_id}", status_code=204)
def deleteFeed(
    token: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    feed_id: int,
):
    if is_admin(token):
        try:
            db_connection.delete_feed(feed_id)
            return
        except ValueError:
            pass

    else:
        response.status_code = 401
        return {"info": "not an Admin"}


class FeedUpdate(BaseModel):
    enabled: Optional[bool] = None


@router.patch("/feeds/{feed_id}", status_code=204)
def update_feed(
    token: Annotated[str, Depends(oauth2_scheme)],
    response: Response,
    feed_id: int,
    update: FeedUpdate,
):
    if not is_admin(token):
        response.status_code = 401
        return {"info": "not an Admin"}

    if update.enabled is not None:
        feed = db_connection.get_feed_from_id(feed_id)
        if update.enabled:
            db_connection.enable_feed(feed)
        else:
            db_connection.disable_feed(feed)


@router.get("/status")
def status():
    return {"status": "okay"}


@router.get("/require_login")
def test_login(token: Annotated[str, Depends(oauth2_scheme)]):
    return jwt.decode(token, config.jwt_secret, algorithms=["HS256"])


app.include_router(router, prefix="/api")
