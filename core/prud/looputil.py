from time import time
from typing import Callable

import pydantic
from loguru import logger
from prud.config import config
from pruddb import PrudDbConnection


class Loop(pydantic.BaseModel):
    interval_s: int
    func: Callable[[PrudDbConnection], None]
    last_exec: int = 0

    def check(self, db_connection: PrudDbConnection, compare_time: int = int(time())):
        if compare_time - self.last_exec > self.interval_s:
            if config.debug_logging:
                logger.debug(f"Calling {self.func.__name__}")
            self.func(db_connection)
            self.last_exec = compare_time


class LoopManager(pydantic.BaseModel):

    class Config:
        arbitrary_types_allowed = True

    db_connection: PrudDbConnection
    _loops: list[Loop] = []

    def import_config(
        self, config_tuple: list[tuple[int, Callable[[PrudDbConnection], None]]]
    ) -> None:
        for interval_s, func in config_tuple:
            self.add_new_loop(
                interval_s=interval_s,
                func=func,
            )

    def add_new_loop(
        self,
        interval_s: int,
        func: Callable[[PrudDbConnection], None],
    ) -> None:
        self._loops.append(Loop(interval_s=interval_s, func=func))

    def check_all_loops(self) -> None:
        current_time = int(time())
        for loop in self._loops:
            loop.check(
                db_connection=self.db_connection,
                compare_time=current_time,
            )
