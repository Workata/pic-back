from pic_back.models import Category


def test_fields():
    category = Category(name="cars")

    assert category.name == "cars"
