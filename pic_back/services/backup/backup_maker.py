import datetime as dt
import typing as t
from pathlib import Path

from pic_back.settings import get_settings


class ZipperInterface(t.Protocol):  # pragma: no cover
    def zip(self, directory_path: Path, output_file_path: Path) -> None:
        pass


class FileUploaderInterface(t.Protocol):  # pragma: no cover
    def upload(self, file_path: Path, parent_folder_id: str, uploaded_file_name: str) -> None:
        pass


class BackupMaker:
    TEMP_BACKUP_DIR_PATH: Path = Path("./data/temp")

    def __init__(self, zipper: ZipperInterface, file_uploader: FileUploaderInterface) -> None:
        self._zipper = zipper
        self._file_uploader = file_uploader
        self._settings = get_settings()

    def make(self, backup_base_name: str = "backup") -> None:
        backup_name = self._get_backup_file_name(backup_base_name)
        backup_file_path = Path(f"{self.TEMP_BACKUP_DIR_PATH}/{backup_name}")
        self._zipper.zip(directory_path=self._settings.database_base_path, output_file_path=backup_file_path)
        self._file_uploader.upload(
            file_path=backup_file_path,
            parent_folder_id=self._settings.google_drive_backup_folder_id,
            uploaded_file_name=backup_name,
        )
        backup_file_path.unlink()

    def _get_backup_file_name(self, backup_base_name: str) -> str:
        backup_name_postfix = dt.datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
        return f"{backup_base_name}_{backup_name_postfix}.zip"
