from pic_back.db.utils.images_db_operations import ImagesDbOperations
from pic_back.models import Image
from pic_back.models.google_drive_folder_content_parsed_data import GoogleDriveFolderContentParsedData
from pic_back.services.google_drive.parsers import GoogleDriveFolderContentDataParser


def test_general_google_data_parser():
    existing_image = Image(id="0123-0123", name="cat.jpg", comment="Nice cat!")
    ImagesDbOperations.create(existing_image)
    data = {
        "files": [
            {"mimeType": "image/jpeg", "id": existing_image.id, "name": existing_image.name},
            {"mimeType": "folder", "id": "0012-1231", "name": "cats"},
            {"mimeType": "image/jpeg", "id": "4350-2134", "name": "dog.jpg"},
        ],
        "nextPageToken": None,
    }

    res = GoogleDriveFolderContentDataParser().parse(data)

    assert type(res) is GoogleDriveFolderContentParsedData
    assert len(res.images) == 2
    assert len(res.folders) == 1
