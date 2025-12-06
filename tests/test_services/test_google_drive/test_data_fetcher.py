from unittest import mock

from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher


@mock.patch("pic_back.services.google_drive.data_fetcher.Credentials")
@mock.patch("pic_back.services.google_drive.data_fetcher.discovery.build")
def test_google_drive_data_fetcher_without_page_token(mock_discovery_build, mock_credentials_cls):
    query = "mimeType = 'application/vnd.google-apps.folder'"
    fields = ["id", "mimeType", "name"]
    page_size = 100
    mock_credentials = mock.Mock()
    mock_credentials_cls.from_authorized_user_file.return_value = mock_credentials
    data_fetcher = GoogleDriveDataFetcher()

    data_fetcher.query_content(query=query, fields=fields, page_size=page_size)

    mock_discovery_build.assert_called_once_with(serviceName="drive", version="v3", credentials=mock_credentials)


@mock.patch("pic_back.services.google_drive.data_fetcher.Credentials")
@mock.patch("pic_back.services.google_drive.data_fetcher.discovery.build")
def test_google_drive_data_fetcher_with_page_token(mock_discovery_build, mock_credentials_cls):
    query = "mimeType = 'application/vnd.google-apps.folder'"
    fields = ["id", "mimeType", "name"]
    page_size = 100
    page_token = "asdf134fadsfasdfdasfasdf"
    mock_credentials = mock.Mock()
    mock_credentials_cls.from_authorized_user_file.return_value = mock_credentials
    data_fetcher = GoogleDriveDataFetcher()

    data_fetcher.query_content(query=query, fields=fields, page_size=page_size, page_token=page_token)

    mock_discovery_build.assert_called_once_with(serviceName="drive", version="v3", credentials=mock_credentials)
