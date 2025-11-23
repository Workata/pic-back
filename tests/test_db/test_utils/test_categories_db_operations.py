import pytest
from tinydb import Query

from pic_back.db.utils.categories_db_operations import CategoriesDbOperations, CategoryNotFoundException
from pic_back.models import Category

query = Query()


def test_delete_existing_category(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    CategoriesDbOperations.delete(category_name=category_name)

    assert categories_db.contains(query.name == category_name) is False


def test_delete_non_existing_category(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    with pytest.raises(CategoryNotFoundException):
        CategoriesDbOperations.delete(category_name="cats")


def test_exists_when_item_exists(categories_db):
    category_name = "cars"
    category = Category(name=category_name)
    categories_db.insert(category.model_dump())
    assert categories_db.contains(query.name == category_name)

    res = CategoriesDbOperations.exists(category_name=category_name)

    assert res is True


def test_exists_when_category_do_not_exist():
    res = CategoriesDbOperations.exists(category_name="kda")

    assert res is False


def test_get_all(categories_db):
    names = ["cars", "cats", "dogs"]
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.count(query.name.matches(r".*")) == 3

    res = CategoriesDbOperations.get_all()

    assert len(res) == 3
    for category in res:
        assert category.name in names


def test_get_when_category_exists(categories_db):
    names = ["cars", "cats", "dogs"]
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.count(query.name.matches(r".*")) == 3

    res = CategoriesDbOperations.get(category_name="cats")

    assert res.name == "cats"


def test_get_when_category_doesnt_exist(categories_db):
    names = ["cars", "cats", "dogs"]
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.count(query.name.matches(r".*")) == 3

    with pytest.raises(CategoryNotFoundException):
        CategoriesDbOperations.get(category_name="flowers")


def test_get_or_create_when_category_exists(categories_db):
    names = ["cars", "cats", "dogs"]
    category = Category(name="cats")
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.count(query.name.matches(r".*")) == 3

    res = CategoriesDbOperations.get_or_create(category)

    assert res == category


def test_get_or_create_when_category_doesnt_exist(categories_db):
    names = ["cars", "dogs"]
    category = Category(name="cats")
    categories = [Category(name=name) for name in names]
    [categories_db.insert(category.model_dump()) for category in categories]
    assert categories_db.contains(query.name == category.name) is False

    res = CategoriesDbOperations.get_or_create(category)

    assert res == category
    assert categories_db.contains(query.name == category.name) is True
