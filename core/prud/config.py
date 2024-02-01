from typing import Literal

from confloader import Config


class PrudConfig(Config):
    db_url: str = "sqlite:////data/polyring.db"
    polyring_members_url: str = "https://polyring.ch/data/members.json"
    discord_username: str = "Polyring Updater"
    avatar_url: str = ""
    feed_request_timeout: int = 15
    webhook_url: str = ""  # VALUE REQUIRED
    ALEMBIC: Literal["local", ""] = ""

    feed_sync_interval_s: int = 21_600  # should be 6 hrs?
    post_sync_interval_s: int = 300  # 5 minutes?
    main_loop_interval_s: int = 250
    re_enable_interval_s: int = 3600
    oldest_post_to_send_ts: int = 0
    env: str = ""


config = PrudConfig(prefix="prud")
