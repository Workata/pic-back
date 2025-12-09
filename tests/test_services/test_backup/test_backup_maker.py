from pathlib import Path
from unittest import mock

from freezegun import freeze_time

from pic_back.services.backup import BackupMaker


@freeze_time("2026-01-14 03:21:34")
@mock.patch.object(Path, "unlink")
def test_backup_maker_flow(mock_path_unlink, settings):
    mock_file_uploader = mock.Mock()
    backup_base_name = "backup"
    mock_zipper = mock.Mock()
    backup_maker = BackupMaker(mock_zipper, mock_file_uploader)
    expected_backup_name = f"{backup_base_name}_14_01_2026__03_21_34.zip"
    expected_zipped_file_path = Path(BackupMaker.TEMP_BACKUP_DIR_PATH, expected_backup_name)

    backup_maker.make()

    mock_zipper.zip.assert_called_once_with(
        directory_path=settings.database_base_path, output_file_path=expected_zipped_file_path
    )
    mock_file_uploader.upload.assert_called_once_with(
        file_path=expected_zipped_file_path,
        parent_folder_id=settings.google_drive_backup_folder_id,
        uploaded_file_name=expected_backup_name,
    )
    mock_path_unlink.assert_called_once_with()
