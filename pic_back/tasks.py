import logging

from fastapi_utils.tasks import repeat_every

from pic_back.services.backup import BackupMakerFactory
from pic_back.services.google_drive import GoogleDriveDiskMapperFactory
from pic_back.settings import EnvType, get_settings
from pic_back.utils.decorators import skip_first_call

settings = get_settings()
logger = logging.getLogger(name="tasks")


@repeat_every(seconds=settings.backup_task_frequency_sec)  # type: ignore
@skip_first_call
async def backup_task() -> None:
    if settings.environment != EnvType.PROD:
        logger.info(f"Backup omitted - not prod. Current env: `{settings.environment.value}`")
        return None
    BackupMakerFactory.create().make()


@repeat_every(seconds=settings.mapper_task_frequency_sec)  # type: ignore
@skip_first_call
async def mapper_task() -> None:
    if settings.environment != EnvType.PROD:
        logger.info(f"Mapping disk omitted - not prod. Current env: `{settings.environment.value}`")
        return None
    GoogleDriveDiskMapperFactory.create().run()


tasks = [backup_task, mapper_task]
