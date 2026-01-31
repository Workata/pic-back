import datetime as dt

import pytest
from tinydb import Query

from pic_back.db.utils import TimestampDbOperations, TimestampExistsException
from pic_back.models import Timestamp

query = Query()


def test_create_when_timestamp_exists(timestamps_db):
    timestamp = Timestamp(name="backup-task-last-run", time=dt.datetime(year=2026, month=1, day=1))
    timestamps_db.insert(timestamp.model_dump())
    assert len(timestamps_db.all()) == 1

    with pytest.raises(TimestampExistsException):
        TimestampDbOperations.create(timestamp)


def test_create_when_timestamp_doesnt_exist(timestamps_db):
    timestamp = Timestamp(name="backup-task-last-run", time=dt.datetime(year=2026, month=1, day=1))
    assert len(timestamps_db.all()) == 0

    TimestampDbOperations.create(timestamp)

    assert len(timestamps_db.all()) == 1
