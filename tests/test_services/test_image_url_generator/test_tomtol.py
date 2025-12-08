from pic_back.services.image_url_generator import TomtolImageUrlGenerator


def test_tomtol_image_url_generator_without_page_token(settings):
    folder_id = "0123-0123"
    img_id = "567-567"

    url = TomtolImageUrlGenerator.generate(folder_id=folder_id, img_id=img_id)

    assert url == f"{settings.frontend_base_url}/#/album/{folder_id}/{img_id}"


def test_tomtol_image_url_generator_with_page_token(settings):
    folder_id = "0123-0123"
    img_id = "567-567"
    page_token = "aasdfasdfdifbjoihuuh4o123oi"

    url = TomtolImageUrlGenerator.generate(folder_id=folder_id, img_id=img_id, page_token=page_token)

    assert url == f"{settings.frontend_base_url}/#/album/{folder_id}/{img_id}?page={page_token}"
