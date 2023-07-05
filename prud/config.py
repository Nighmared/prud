import os

discord_username = os.environ.get("WEBHOOK_USERNAME", default="Polyring Updater")
avatar_url = None
webhook_url = "https://discord.com/api/webhooks/1126076340173545512/b0gEKj8yuYFLEx1Qas7UxdAteSVLE6OPKak1cP2fXGkOlmaadCjayGFwQS5Qy_45jyCk"
db_url = "sqlite:///polyring.db"
polyring_members_url = "https://polyring.ch/data/members.json"

feed_request_timeout = 5
