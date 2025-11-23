import pytest
from tinydb import Query

from pic_back.db.utils.markers_db_operations import MarkerExistsException, MarkersDbOperations
from pic_back.models import Coords, Marker

query = Query()


def test_create_when_marker_exists(markers_db):
    coords = Coords(latitude=42.123456, longitude=30.654321)
    marker = Marker(coords=coords, url="www.pics.com/312312312")
    markers_db.insert(marker.model_dump())
    assert len(markers_db.all()) == 1

    with pytest.raises(MarkerExistsException):
        MarkersDbOperations.create(marker)


def test_create_when_marker_doesnt_exist(markers_db):
    coords = Coords(latitude=42.123456, longitude=30.654321)
    marker = Marker(coords=coords, url="www.pics.com/312312312")
    assert len(markers_db.all()) == 0

    res = MarkersDbOperations.create(marker)

    assert res == marker
    assert len(markers_db.all()) == 1


def test_get_all_markers(markers_db):
    coords = Coords(latitude=42.123456, longitude=30.654321)
    marker = Marker(coords=coords, url="www.pics.com/312312312")
    markers_db.insert(marker.model_dump())
    assert len(markers_db.all()) == 1

    res = MarkersDbOperations.get_all()

    assert res == [marker]
    assert len(markers_db.all()) == 1
