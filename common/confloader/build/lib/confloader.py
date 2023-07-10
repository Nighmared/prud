import os


class Config:
    def __init__(self, prefix: str) -> None:
        cls = self.__class__
        for k in cls.__dict__.keys():
            env_v = os.environ.get(prefix.upper() + "_" + k.upper())
            if env_v is not None:
                if cls.__annotations__[k] == int:
                    self.__dict__[k] = int(env_v)
                else:
                    self.__dict__[k] = env_v
                continue
