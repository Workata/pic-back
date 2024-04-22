from src.services.backups.backup_maker import BackupMaker
from src.services.backups.zipper import Zipper
from src.services.backups.file_uploader import FileUploader


class BackupMakerFactory:
    @classmethod
    def create(cls) -> BackupMaker:
        return BackupMaker(zipper=Zipper(), file_uploader=FileUploader())
