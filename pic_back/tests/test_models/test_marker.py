from pic_back.models import Marker, Coords
from assertpy import assert_that


def test_model_fields():
    marker = Marker(coords=Coords(latitude=42.123456, longitude=30.654321), url="www.pics.com/312312312")
    assert_that(marker.coords.latitude).is_equal_to(42.123456)
    assert_that(marker.coords.longitude).is_equal_to(30.654321)
    assert_that(marker.url).is_equal_to("www.pics.com/312312312")
