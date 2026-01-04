from unittest import mock

from pic_back.models import Coords
from pic_back.services.google_drive.images_mapper import GoogleDriveImagesMapper

# TODO extend test cases


def test_images_mapper_without_page_token_when_coords_found():
    mock_data_fetcher = mock.Mock()
    mock_data = {
        "files": [
            {"mimeType": "image/jpeg", "id": "012"},
            {"mimeType": "folder", "id": "0123-0123"},
            {"mimeType": "image/jpeg", "id": "013"},
        ]
    }
    mock_data_fetcher.query_content.return_value = mock_data
    mock_coords_getter = mock.Mock()
    mock_coords_getter.get_coords.return_value = Coords(latitude=123.123, longitude=45.324)
    folder_id = "0123-0123"
    images_mapper = GoogleDriveImagesMapper(data_fetcher=mock_data_fetcher)

    images_mapper.map_folder(folder_id)


def test_images_mapper_with_page_token_when_coords_found():
    mock_data_fetcher = mock.Mock()
    mock_data_first_page = {
        "files": [
            {"mimeType": "image/jpeg", "id": "012"},
            {"mimeType": "folder", "id": "0123-0123"},
            {"mimeType": "image/jpeg", "id": "013"},
        ],
        "nextPageToken": "asdfasdifoiu1hn3o4ij1",
    }
    mock_data_next_page = {
        "files": [
            {"mimeType": "image/jpeg", "id": "012"},
            {"mimeType": "folder", "id": "0123-0123"},
            {"mimeType": "image/jpeg", "id": "013"},
        ]
    }
    mock_data_fetcher.query_content.side_effect = [mock_data_first_page, mock_data_next_page]
    mock_coords_getter = mock.Mock()
    mock_coords_getter.get_coords.return_value = Coords(latitude=123.123, longitude=45.324)
    folder_id = "0123-0123"
    images_mapper = GoogleDriveImagesMapper(data_fetcher=mock_data_fetcher)

    images_mapper.map_folder(folder_id)


def test_images_mapper_without_page_token_when_coords_not_found():
    mock_data_fetcher = mock.Mock()
    mock_data = {
        "files": [
            {"mimeType": "image/jpeg", "id": "012"},
            {"mimeType": "folder", "id": "0123-0123"},
            {"mimeType": "image/jpeg", "id": "013"},
        ]
    }
    mock_data_fetcher.query_content.return_value = mock_data
    mock_coords_getter = mock.Mock()
    mock_coords_getter.get_coords.return_value = None
    folder_id = "0123-0123"
    images_mapper = GoogleDriveImagesMapper(data_fetcher=mock_data_fetcher)

    images_mapper.map_folder(folder_id)
