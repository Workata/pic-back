from pic_back.models import GoogleDriveFolderContentParsedData


def test_model_dump():
    next_page_token_value = "asdfsdafsad"
    expected_dump = {"images": [], "folders": [], "nextPageToken": next_page_token_value}

    folder_content = GoogleDriveFolderContentParsedData(images=[], folders=[], next_page_token=next_page_token_value)

    assert folder_content.model_dump() == expected_dump
