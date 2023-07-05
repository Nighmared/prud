import os

discord_username = os.environ.get("WEBHOOK_USERNAME", default="Polyring Updater")
avatar_url = None
webhook_url = ""
with open("webhook.txt", "r") as f:
    webhook_url = f.readline()
db_url = "sqlite:///polyring.db"
polyring_members_url = "https://polyring.ch/data/members.json"

feed_request_timeout = 5
