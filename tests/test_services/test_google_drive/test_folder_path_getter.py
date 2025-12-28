from unittest import mock

from pic_back.services.google_drive import GoogleDriveFolderPathGetter


@mock.patch("pic_back.services.google_drive.folder_path_getter.GoogleDriveServiceFactory")
def test_folder_path_getter_flow_when_folder_has_no_parent(mock_service_factory_cls):
    folder_id = "1230123901283"
    folder_name = "Africa"
    mock_gdrive_service = mock.Mock()
    mock_target_folder = {"id": folder_id, "name": folder_name}
    mock_gdrive_service.files.return_value.get.return_value.execute.return_value = mock_target_folder
    mock_service_factory_cls.create.return_value = mock_gdrive_service
    folder_path_getter = GoogleDriveFolderPathGetter()

    res = folder_path_getter.get(folder_id)

    assert len(res) == 1
    assert res[0].id == folder_id
    assert res[0].name == folder_name
