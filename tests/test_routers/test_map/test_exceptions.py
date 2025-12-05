from pic_back.routers.map.exceptions import MarkerExistsHTTPException


def test_marker_exists_exception():
    lat = 1.2
    lon = 3.2

    exc = MarkerExistsHTTPException(lat=lat, lon=lon)

    assert (
        exc.detail
        == f"Marker with lat '{lat}' and lon '{lon}' coords already exists. Please provide different coordinates."
    )
