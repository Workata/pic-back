from unittest import mock

from pic_back.services.google_drive import GoogleDriveImagesMapperFactory

mock_path = "pic_back.services.google_drive.images_mapper_factory"


@mock.patch(f"{mock_path}.GoogleDriveDataFetcher")
@mock.patch(f"{mock_path}.GoogleDriveImagesMapper")
def test_google_drive_images_mapper_factory(mock_images_mapper, mock_data_fetcher):
    res = GoogleDriveImagesMapperFactory.create()

    mock_images_mapper.assert_called_once_with(data_fetcher=mock_data_fetcher.return_value)
    assert res == mock_images_mapper.return_value
