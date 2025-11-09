from pic_back.services.backup.backup_maker import BackupMaker
from pic_back.services.backup.file_uploader import FileUploader
from pic_back.services.backup.zipper import Zipper


class BackupMakerFactory:
    @classmethod
    def create(cls) -> BackupMaker:
        return BackupMaker(zipper=Zipper(), file_uploader=FileUploader())
