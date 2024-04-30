from services.backup.backup_maker import BackupMaker
from services.backup.zipper import Zipper
from services.backup.file_uploader import FileUploader


class BackupMakerFactory:
    @classmethod
    def create(cls) -> BackupMaker:
        return BackupMaker(zipper=Zipper(), file_uploader=FileUploader())
