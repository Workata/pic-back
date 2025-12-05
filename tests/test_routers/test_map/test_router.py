from unittest import mock

from fastapi import status

from pic_back.db.utils import MarkersDbOperations
from pic_back.models import Coords, Marker
from pic_back.routers.map.router import map_folder_task

images_router_base_path = "/api/v1/map"


def test_list_markers_endpoint_should_return_200(client):
    markers = [
        Marker(url="www.dummy.com", coords=Coords(latitude="4.1", longitude="3.2")),
        Marker(url="www.dummy2.com", coords=Coords(latitude="3.5", longitude="1.7")),
    ]
    [MarkersDbOperations.create(marker) for marker in markers]

    res = client.get(f"{images_router_base_path}/marker")

    res_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert len(res_data) == len(markers)


def test_create_marker_endpoint_should_return_201(client, auth_headers):
    marker = Marker(url="www.dummy.com", coords=Coords(latitude="4.1", longitude="3.2"))

    res = client.post(f"{images_router_base_path}/marker", data=marker.model_dump_json(), headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_201_CREATED
    assert (
        res_data["detail"]
        == f"Marker created for (lat: {marker.coords.latitude}, lon: {marker.coords.longitude}) with url: '{marker.url}'."
    )


def test_create_marker_endpoint_should_return_400_when_it_already_exists(client, auth_headers):
    marker = Marker(url="www.dummy.com", coords=Coords(latitude="4.1", longitude="3.2"))
    MarkersDbOperations.create(marker)

    res = client.post(f"{images_router_base_path}/marker", data=marker.model_dump_json(), headers=auth_headers)

    res_data = res.json()
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        res_data["detail"]
        == f"Marker with lat '{marker.coords.latitude}' and lon '{marker.coords.longitude}' coords already exists. Please provide different coordinates."
    )


@mock.patch("pic_back.routers.map.router.GoogleDriveImagesMapperFactory")
def test_map_folder_task(mock_mapper_factory_cls):
    folder_id = "0123-0123"
    mock_mapper = mock.Mock()
    mock_mapper_factory_cls.create.return_value = mock_mapper

    map_folder_task(folder_id)

    mock_mapper_factory_cls.create.assert_called_once()
    mock_mapper.map_folder.assert_called_once_with(folder_id)


@mock.patch("pic_back.routers.map.router.map_folder_task")
def test_map_folder_endpoint(mock_map_folder_task_func, client, auth_headers):
    folder_id = "0123-0123"

    res = client.post(f"{images_router_base_path}/folder/{folder_id}", headers=auth_headers)

    res_data = res.json()
    mock_map_folder_task_func.assert_called_once_with(folder_id)
    assert res_data["detail"] == f"Folder {folder_id} will be mapped in the background!"
