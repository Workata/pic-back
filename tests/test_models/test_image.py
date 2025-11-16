from pic_back.models import Image


def test_fields():
    id = "01213-12314-53463"
    name = "sakura.jpg"

    image = Image(id=id, name=name)

    assert image.id == id
    assert image.name == name
    assert image.categories == []
    assert image.comment == ""
