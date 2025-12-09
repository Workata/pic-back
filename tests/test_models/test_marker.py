from pic_back.models import Coords, Marker


def test_model_fields():
    expected_latitude = 42.123457
    expected_longitude = 30.654321

    marker = Marker(coords=Coords(latitude=42.12345678, longitude=30.65432123), url="www.pics.com/312312312")

    assert marker.coords.latitude == expected_latitude
    assert marker.coords.longitude == expected_longitude
    assert marker.url == "www.pics.com/312312312"
    assert str(marker.coords) == f"lat: {expected_latitude}, lon: {expected_longitude}"
