from unittest import mock

from pic_back.services.google_drive.data_fetcher import GoogleDriveDataFetcher


@mock.patch("pic_back.services.google_drive.data_fetcher.GoogleDriveServiceFactory")
def test_google_drive_data_fetcher_flow_without_page_token(mock_service_factory_cls):
    query = "mimeType = 'application/vnd.google-apps.folder'"
    fields = ["id", "mimeType", "name"]
    page_size = 100
    mock_gdrive_service = mock.Mock()
    mock_service_factory_cls.create.return_value = mock_gdrive_service
    data_fetcher = GoogleDriveDataFetcher()

    data_fetcher.query_content(query=query, fields=fields, page_size=page_size)


@mock.patch("pic_back.services.google_drive.data_fetcher.GoogleDriveServiceFactory")
def test_google_drive_data_fetcher_flow_with_page_token(mock_service_factory_cls):
    query = "mimeType = 'application/vnd.google-apps.folder'"
    fields = ["id", "mimeType", "name"]
    page_size = 100
    page_token = "asdf134fadsfasdfdasfasdf"
    mock_gdrive_service = mock.Mock()
    mock_service_factory_cls.create.return_value = mock_gdrive_service
    data_fetcher = GoogleDriveDataFetcher()

    data_fetcher.query_content(query=query, fields=fields, page_size=page_size, page_token=page_token)
