from confloader import Config


class ApiConfig(Config):
    db_url: str = "sqlite:////data/polyring.db"


config = ApiConfig("api")
