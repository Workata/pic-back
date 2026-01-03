from unittest import mock

from pic_back.services.google_drive import GoogleDriveServiceFactory


@mock.patch("pic_back.services.google_drive.google_drive_service_factory.Credentials.from_authorized_user_file")
@mock.patch("pic_back.services.google_drive.google_drive_service_factory.discovery.build")
def test_flow(mock_discovery_build, mock_from_auth_user_file):
    scopes = ["drive.read"]

    GoogleDriveServiceFactory.create(scopes)

    mock_from_auth_user_file.assert_called_once()
    mock_discovery_build.assert_called_once()
