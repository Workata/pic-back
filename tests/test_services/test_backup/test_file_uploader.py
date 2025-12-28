from pathlib import Path
from unittest import mock

from pic_back.services.backup.file_uploader import FileUploader


@mock.patch("pic_back.services.backup.file_uploader.GoogleDriveServiceFactory")
def test_file_uploader_flow(mock_service_factory_cls, tmp_path):
    parent_folder_id = "0123-0123"
    uploaded_file_name = "backup.zip"
    file_path = Path(tmp_path, uploaded_file_name)
    file_path.touch()
    mock_gdrive_service = mock.Mock()
    mock_service_factory_cls.create.return_value = mock_gdrive_service
    file_uploader = FileUploader()

    file_uploader.upload(file_path=file_path, parent_folder_id=parent_folder_id, uploaded_file_name=uploaded_file_name)
