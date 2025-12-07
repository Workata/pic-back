from pic_back.services.google_drive.parsers import GoogleDriveImageIdsDataParser


def test_ids_data_parser():
    expected_ids = ["2345-2345", "51-51"]
    data = {
        "files": [
            {"mimeType": "image/jpeg", "id": expected_ids[0]},
            {"mimeType": "folder", "id": "0123-0123"},
            {"mimeType": "image/jpeg", "id": expected_ids[1]},
        ]
    }
    ids_data_parser = GoogleDriveImageIdsDataParser()

    ids = ids_data_parser.parse(data)

    assert ids == expected_ids
