from unittest import mock

from fastapi import status

from pic_back.routers.gdrive.serializers.output import GoogleDriveFolderContentOutputSerializer

mock_base_path = "pic_back.routers.gdrive.router"
gdrive_router_base_path = "/api/v1/gdrive"


@mock.patch(f"{mock_base_path}.GoogleDriveFolderContentParser")
@mock.patch(f"{mock_base_path}.GoogleDriveDataFetcher")
def test_get_folder_content_should_return_200(mock_data_fetcher_cls, mock_data_parser_cls, client):
    folder_id = "0123-0123"
    mock_data_parser_cls().parse.return_value = GoogleDriveFolderContentOutputSerializer(
        images=[], folders=[], next_page_token=None
    )

    res = client.get(f"{gdrive_router_base_path}/folder/{folder_id}")

    assert res.status_code == status.HTTP_200_OK
