from pathlib import Path
from unittest import mock

from pic_back.services.backup.file_uploader import FileUploader


@mock.patch("pic_back.services.backup.file_uploader.Credentials")
@mock.patch("pic_back.services.backup.file_uploader.discovery.build")
def test_file_uploader(mock_discovery_build, mock_credentials_cls, tmp_path):
    parent_folder_id = "0123-0123"
    uploaded_file_name = "backup.zip"
    file_path = Path(tmp_path, uploaded_file_name)
    file_path.touch()
    mock_credentials = mock.Mock()
    mock_credentials_cls.from_authorized_user_file.return_value = mock_credentials
    file_uploader = FileUploader()

    file_uploader.upload(file_path=file_path, parent_folder_id=parent_folder_id, uploaded_file_name=uploaded_file_name)

    mock_discovery_build.assert_called_once_with(serviceName="drive", version="v3", credentials=mock_credentials)
