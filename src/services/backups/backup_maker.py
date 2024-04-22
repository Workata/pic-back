import datetime as dt
import os
import typing as t


class ZipperInterface(t.Protocol):
    def zip(self, directory_path: str, output_file_path: str) -> None:
        pass


class FileUploaderInterface(t.Protocol):
    def upload(self, file_path: str, parent_folder_id: str, uploaded_file_name: str) -> None:
        pass


class BackupMaker:
    DATA_DIR_PATH: str = r"./data/database"
    TEMP_BACKUP_DIR_PATH: str = r"./data/temp"
    BACKUP_NAME_PREFIX: str = "backup"
    BACKUP_G_DRIVE_FOLDER_ID: str = "19W3Pw2O_9UyfzFEm3JSR4ShxMyeB1U-5"

    def __init__(self, zipper: ZipperInterface, file_uploader: FileUploaderInterface) -> None:
        self._zipper = zipper
        self._file_uploader = file_uploader

    def make(self) -> None:
        backup_name = self._get_backup_file_name()
        backup_file_path = f"{self.TEMP_BACKUP_DIR_PATH}/{backup_name}"
        self._zipper.zip(directory_path=self.DATA_DIR_PATH, output_file_path=backup_file_path)
        self._file_uploader.upload(
            file_path=backup_file_path, parent_folder_id=self.BACKUP_G_DRIVE_FOLDER_ID, uploaded_file_name=backup_name
        )
        self._delete_file(backup_file_path)

    def _get_backup_file_name(self) -> str:
        backup_name_postfix = dt.datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        return f"{self.BACKUP_NAME_PREFIX}_{backup_name_postfix}.zip"

    def _delete_file(self, file_path: str) -> None:
        os.remove(file_path)
