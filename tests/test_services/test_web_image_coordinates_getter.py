from unittest import mock

from pic_back.services.web_image_coordinates_getter import WebImageCoordinatesGetter

data_base_path_str: str = "./tests/data"


@mock.patch("pic_back.services.web_image_coordinates_getter.httpx.get")
@mock.patch("pic_back.services.web_image_coordinates_getter.io.BytesIO")
def test_web_image_coords_getter_from_image_with_exif_coords(mock_bytes_io_cls, mock_httpx_get):
    img_url = "www.dummy.com/images/img.jpg"
    with open(f"{data_base_path_str}/image_with_exif_coords_data.jpg", "rb") as img:
        mock_bytes_io_cls.return_value = img
        coords_getter = WebImageCoordinatesGetter()

        coords = coords_getter.get_coords(img_url)

        assert coords.latitude == 43.467082
        assert coords.longitude == 11.884538


@mock.patch("pic_back.services.web_image_coordinates_getter.httpx.get")
@mock.patch("pic_back.services.web_image_coordinates_getter.io.BytesIO")
def test_web_image_coords_getter_from_image_with_exif_but_no_coords(mock_bytes_io_cls, mock_httpx_get):
    img_url = "www.dummy.com/images/img.jpg"
    with open(f"{data_base_path_str}/image_with_exif_but_no_coords_data.jpg", "rb") as img:
        mock_bytes_io_cls.return_value = img
        coords_getter = WebImageCoordinatesGetter()

        coords = coords_getter.get_coords(img_url)

        assert coords is None


@mock.patch("pic_back.services.web_image_coordinates_getter.httpx.get")
@mock.patch("pic_back.services.web_image_coordinates_getter.io.BytesIO")
def test_web_image_coords_getter_from_image_without_exif(mock_bytes_io_cls, mock_httpx_get):
    img_url = "www.dummy.com/images/img.jpg"
    with open(f"{data_base_path_str}/image_without_exif.jpg", "rb") as img:
        mock_bytes_io_cls.return_value = img
        coords_getter = WebImageCoordinatesGetter()

        coords = coords_getter.get_coords(img_url)

        assert coords is None
