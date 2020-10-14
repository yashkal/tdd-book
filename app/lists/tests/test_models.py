import pytest
from django.core.exceptions import ValidationError
from lists.models import Item, List

pytestmark = pytest.mark.django_db


def test_saving_and_retrieving_items():
    list_ = List()
    list_.save()

    first_item = Item()
    first_item.text = "The first (ever) list item"
    first_item.list = list_
    first_item.save()

    second_item = Item()
    second_item.text = "Item the second"
    second_item.list = list_
    second_item.save()

    saved_list = List.objects.first()
    assert saved_list == list_

    saved_items = Item.objects.all()
    assert saved_items.count() == 2

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    assert first_saved_item.text == "The first (ever) list item"
    assert first_saved_item.list == list_
    assert second_saved_item.text == "Item the second"
    assert second_saved_item.list == list_


def test_cannot_save_empty_list_items():
    list_ = List.objects.create()
    item = Item(list=list_, text="")
    with pytest.raises(ValidationError):
        item.save()
        item.full_clean()


def test_get_absolute_url():
    list_ = List.objects.create()
    assert list_.get_absolute_url(), f"/lists/{list_.id}/"
