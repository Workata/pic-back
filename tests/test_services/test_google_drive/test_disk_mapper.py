import datetime as dt
from unittest import mock

from freezegun import freeze_time

from pic_back.db.utils import TimestampDbOperations
from pic_back.services.google_drive import GoogleDriveDiskMapper


@freeze_time("2026-01-14 03:21:34")
def test_disk_mapper_flow_when_ther_are_no_folders_found():
    mock_data_fetcher = mock.Mock()
    mock_data_fetcher.query_content.return_value = {"files": []}
    mock_images_mapper = mock.Mock()
    disk_mapper = GoogleDriveDiskMapper(data_fetcher=mock_data_fetcher, images_mapper=mock_images_mapper)

    disk_mapper.run()

    # assert that proper timestamp was created in the DB
    timestamp = TimestampDbOperations.get(GoogleDriveDiskMapper.TIMESTAMP_NAME)
    assert timestamp.time == dt.datetime.now(dt.timezone.utc)
