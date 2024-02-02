from typing import Literal

from confloader import Config


class PrudConfig(Config):
    db_url: str = "sqlite:////data/polyring.db"
    polyring_members_url: str = "https://polyring.ch/data/members.json"
    discord_username: str = "Polyring Updater"
    avatar_url: str = ""
    feed_request_timeout: int = 15
    webhook_url: str = ""  # VALUE REQUIRED
    alembic: Literal["local", ""] = ""

    feed_sync_interval_s: int = 21_600  # should be 6 hrs?
    post_sync_interval_s: int = 300  # 5 minutes?
    main_loop_interval_s: int = 5  # not really important to keep this high
    feed_disable_backoff_step_s: int = 3600  # start at 1h, then 2h ...
    feed_reenable_interval_s: int = 1800  # 30 mins, good enough
    recover_backoff_interval_s: int = 43_200  # 2*21600 = 12 hrs?
    oldest_post_to_send_ts: int = 0
    env: str = ""
    debug_logging: bool = False


config = PrudConfig(prefix="prud")
