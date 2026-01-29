from pic_back.services.backup import BackupMakerFactory
from pic_back.services.google_drive import GoogleDriveDiskMapperFactory
from pic_back.settings import get_settings
from pic_back.shared import EnvType
from pic_back.utils.decorators import only_on_envs, repeat_every, skip_first_call

settings = get_settings()

"""
Tasks are called at the beginning of the application lifespan and then repeated every X seconds.
To skip the first call (application startup) use `skip_first_call` decorator.
Tasks should accept no arguments and return nothing.

> This design is not ideal so it might change.

If you create a new task add it to the `tasks` list.
"""


@repeat_every(seconds=settings.backup_task_frequency_sec)
@skip_first_call
@only_on_envs(envs=[EnvType.PROD])
async def backup_task() -> None:
    BackupMakerFactory.create().make()


@repeat_every(seconds=settings.mapper_task_frequency_sec)
@skip_first_call
@only_on_envs(envs=[EnvType.PROD])
async def mapper_task() -> None:
    GoogleDriveDiskMapperFactory.create().run()


tasks = [backup_task, mapper_task]
