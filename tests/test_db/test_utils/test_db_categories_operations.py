import pytest
from tinydb import Query

from pic_back.db.utils.db_categories_operations import CategoryNotFoundException, DbCategoriesOperations
from pic_back.models import Category

query = Query()


def test_delete_existing_category(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    DbCategoriesOperations.delete(category_name=category_name)

    assert categories_db.contains(query.name == category_name) is False


def test_delete_non_existing_category(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    with pytest.raises(CategoryNotFoundException):
        DbCategoriesOperations.delete(category_name="cats")


def test_exists_when_item_exists(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    res = DbCategoriesOperations.exists(category_name=category_name)

    assert res is True


def test_exists_when_item_do_not_exist():
    res = DbCategoriesOperations.exists(category_name="kda")

    assert res is False


def test_get_all(categories_db):
    names = ["cars", "cats", "dogs"]
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.count(query.name.matches(r".*")) == 3

    res = DbCategoriesOperations.get_all()

    assert len(res) == 3
    for category in res:
        assert category.name in names
