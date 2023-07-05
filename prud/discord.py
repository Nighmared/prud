from datetime import datetime
from enum import Enum
from typing import Optional

import requests
from pydantic import BaseModel, root_validator

from prud import config


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
    type: Optional[EmbedType] = None
    description: Optional[str] = None
    url: Optional[str] = None
    timestamp: Optional[datetime] = None
    color: Optional[int] = None
    footer: Optional[EmbedFooter] = None
    image: Optional[EmbedImage] = None
    thumbnail: Optional[EmbedThumbnail] = None
    video: Optional[EmbedVideo] = None
    provider: Optional[EmbedProvider] = None
    author: Optional[EmbedAuthor] = None
    fields: Optional[list[EmbedField]] = None


class WebhookObject(BaseModel):
    content: Optional[str]
    username: Optional[str] = config.discord_username
    avatar_url: Optional[str] = config.avatar_url
    embeds: Optional[list[Embed]] = []

    @root_validator()
    def verify_has_content(cls, values):
        content = values.get("content")
        embeds = values.get("embeds")
        file = values.get("files")

        if content is None and embeds is None and file is None:
            raise ValueError("WebhookObject must have one of content,file,embeds")
        return values


def send_to_webhook(content: WebhookObject):
    requests.post(url=config.webhook_url, json=content.dict())
