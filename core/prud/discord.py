from datetime import datetime
from enum import Enum
from typing import Iterable, Optional, Self

import pruddb
import requests
from loguru import logger
from prud.config import config
from pydantic import BaseModel, ValidationError, model_validator


class PostException(Exception):
    pass


class EmbedType(Enum):
    RICH = "rich"
    IMAGE = "image"
    VIDEO = "video"
    GIFV = "gifv"
    ARTICLE = "article"
    LINK = "link"


class EmbedFooter(BaseModel):
    text: str
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


class EmbedAttachmentBase(BaseModel):
    url: str
    proxy_url: Optional[str] = None
    height: Optional[int] = None
    width: Optional[int] = None


class EmbedImage(EmbedAttachmentBase):
    pass


class EmbedThumbnail(EmbedAttachmentBase):
    pass


class EmbedVideo(EmbedAttachmentBase):
    pass


class EmbedProvider(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None


class EmbedAuthor(BaseModel):
    name: str
    url: Optional[str] = None
    icon_url: Optional[str] = None
    proxy_icon_url: Optional[str] = None


class EmbedField(BaseModel):
    name: str
    vaule: str
    inline: Optional[bool] = None


class Embed(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = "rich"
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[str] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[list[EmbedField]] = None

    @staticmethod
    def from_post(post: pruddb.PolyRingPost, db_connection: pruddb.PrudDbConnection):
        feed = db_connection.get_feed_from_id(post.feed_id)
        author = EmbedAuthor(name=feed.title, url=feed.url)
        provider = EmbedProvider(name="nighmared", url="https://nighmared.tech")
        footer = EmbedFooter(
            text="<3",
        )
        published = datetime.fromtimestamp(post.published).isoformat()
        embed = Embed(
            title=post.title,
            url=post.link,
            description=post.summary[:200],
            timestamp=published,
            author=author,
            provider=provider,
            footer=footer,
        )
        return embed


class WebhookPostObject(BaseModel):
    content: Optional[str] = None
    username: Optional[str] = config.discord_username
    avatar_url: Optional[str] = config.avatar_url
    embeds: Optional[list[Embed]] = []

    @model_validator(mode="after")
    def verify_has_content(self) -> Self:
        if self.content is None and self.embeds is None:
            raise ValidationError("WebhookObject must have either of content or embeds")
        return self

    @staticmethod
    def from_post(
        post: pruddb.PolyRingPost, db_connection: pruddb.PrudDbConnection
    ) -> "WebhookPostObject":
        embed = Embed.from_post(post, db_connection)
        webhook = WebhookPostObject(
            username=config.discord_username,
            avatar_url=config.avatar_url,
            embeds=[
                embed,
            ],
        )
        return webhook


def _value_cleaner(v):
    if type(v) is dict:
        res = _dict_cleaner(v)
        if len(res) == 0:
            return None
        else:
            return res
    if type(v) is list:
        res = _list_cleaner(v)
        if len(res) == 0:
            return None
        return res
    return v


def _list_cleaner(v: Iterable):
    return [_value_cleaner(e) for e in v]


def _dict_cleaner(d: dict) -> dict:
    new_dict = {}
    for k, v in d.items():
        new_v = _value_cleaner(v)
        if new_v is None:
            continue
        new_dict[k] = new_v
    return new_dict


def send_to_webhook(content: WebhookPostObject):
    if config.env == "dev":
        logger.info("Not actually sending because dev environment :)")
        return

    webhook_dict = content.dict()
    resp = requests.post(url=config.webhook_url, json=webhook_dict, timeout=10)
    if resp.status_code // 100 != 2:
        logger.debug("Got error status back from discord")
        logger.debug(resp.json())
        raise PostException(
            f"Got non 2xx status code from discord ({resp.status_code})"
        )
