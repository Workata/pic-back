from unittest import mock

from pic_back.services.backup import BackupMakerFactory


@mock.patch("pic_back.services.backup.backup_maker_factory.FileUploader")
@mock.patch("pic_back.services.backup.backup_maker_factory.Zipper")
@mock.patch("pic_back.services.backup.backup_maker_factory.BackupMaker")
def test_backup_maker_factory(mock_backup_maker_cls, zipper_cls, file_uploader_cls):
    res = BackupMakerFactory.create()

    mock_backup_maker_cls.assert_called_once_with(
        zipper=zipper_cls.return_value, file_uploader=file_uploader_cls.return_value
    )
    assert res == mock_backup_maker_cls.return_value
