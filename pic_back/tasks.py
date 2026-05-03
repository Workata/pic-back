from typing import List

from pic_back.models import RepeatedTask
from pic_back.services.backup import BackupMakerFactory
from pic_back.services.google_drive import GoogleDriveDiskMapperFactory
from pic_back.settings import get_settings
from pic_back.shared import EnvType
from pic_back.utils.decorators import only_on_envs

settings = get_settings()

"""
Tasks are called at the beginning of the application lifespan and then repeated every X seconds.
Tasks should accept no arguments and return nothing.

> This design is not ideal so it might change.

If you create a new task add it to the `tasks` list.
"""


@only_on_envs(envs=[EnvType.PROD])
async def backup_task() -> None:
    BackupMakerFactory.create().make()


@only_on_envs(envs=[EnvType.PROD])
async def mapper_task() -> None:
    GoogleDriveDiskMapperFactory.create().run()


tasks: List[RepeatedTask] = [
    RepeatedTask(func=backup_task, interval_sec=settings.backup_task_frequency_sec),
    RepeatedTask(func=mapper_task, interval_sec=settings.mapper_task_frequency_sec),
]
