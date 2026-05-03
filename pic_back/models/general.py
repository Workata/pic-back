from typing import Callable

from pydantic import BaseModel


class HealthcheckStatus(BaseModel):
    status: str


class SystemInfo(BaseModel):
    version: str


class RepeatedTask(BaseModel):
    func: Callable
    interval_sec: int
