import os


class Config:
    db_url: str = "sqlite:////data/polyring.db"
    polyring_members_url: str = "https://polyring.ch/data/members.json"
    discord_username: str = "Polyring Updater"
    avatar_url: str = ""
    feed_request_timeout: int = 5
    webhook_url: str = ""  # VALUE REQUIRED

    feed_sync_interval_s: int = 21_600  # should be 6 hrs?
    post_sync_interval_s: int = 300  # 5 minutes?
    main_loop_interval_s: int = 250

    oldest_post_to_send_ts: int = 0

    def __init__(self) -> None:
        for k in Config.__dict__.keys():
            env_v = os.environ.get("PRUD_" + k.upper())
            if env_v is not None:
                if Config.__annotations__[k] == int:
                    self.__dict__[k] = int(env_v)
                else:
                    self.__dict__[k] = env_v
                continue


config = Config()
