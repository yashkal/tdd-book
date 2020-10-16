import pytest
from django.core.exceptions import ValidationError
from lists.models import Item, List

pytestmark = pytest.mark.django_db


class ItemModelTest:
    def test_default_text(self):
        item = Item()
        assert item.text == ""

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        assert item in list_.item_set.all()

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text="")
        with pytest.raises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="bla")
        with pytest.raises(ValidationError):
            item = Item(list=list_, text="bla")
            item.full_clean()

    def test_can_save_same_item_to_different_lists(self):
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(list=list1, text="bla")
        item = Item(list=list2, text="bla")
        item.full_clean()  # Should not raise

    def test_list_ordering(self):
        list_ = List.objects.create()
        item_1 = Item.objects.create(text="i1", list=list_)
        item_2 = Item.objects.create(text="item 2", list=list_)
        item_3 = Item.objects.create(text="3", list=list_)
        assert list(Item.objects.all()) == [item_1, item_2, item_3]

    def test_string_representation(self):
        item = Item(text="Some text")
        assert str(item) == "Some text"


class ListModelTest:
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        assert list_.get_absolute_url(), f"/lists/{list_.id}/"
