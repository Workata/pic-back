from pic_back.routers.gdrive.serializers.output import GoogleDriveFolderContentOutputSerializer


def test_model_dump():
    next_page_token_value = "asdfsdafsad"
    expected_dump = {"images": [], "folders": [], "nextPageToken": next_page_token_value}

    folder_content = GoogleDriveFolderContentOutputSerializer(
        images=[], folders=[], next_page_token=next_page_token_value
    )

    assert folder_content.model_dump() == expected_dump
