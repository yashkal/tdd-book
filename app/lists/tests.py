import pytest
from django.test import SimpleTestCase
from lists.models import Item, List
from pytest_django import asserts as test


class TestHomePage:
    def test_uses_home_template(self, client):
        response = client.get("/")
        test.assertTemplateUsed(response, "home.html")


@pytest.mark.django_db
class TestListAndItemModel:
    def test_saving_and_retrieving_items(self):
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


@pytest.mark.django_db
class TestListView:
    def test_uses_list_template(self, client):
        list_ = List.objects.create()
        response = client.get(f"/lists/{list_.id}/")
        test.assertTemplateUsed(response, "list.html")

    def test_displays_only_items_for_that_list(self, client):
        correct_list = List.objects.create()
        Item.objects.create(text="itemey 1", list=correct_list)
        Item.objects.create(text="itemey 2", list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text="other item 1", list=other_list)
        Item.objects.create(text="other item 2", list=other_list)

        response = client.get(f"/lists/{correct_list.id}/")

        test.assertContains(response, "itemey 1")
        test.assertContains(response, "itemey 2")
        test.assertNotContains(response, "other item 1")
        test.assertNotContains(response, "other item 2")

    def test_passes_correct_list_to_template(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = client.get(f"/lists/{correct_list.id}/")
        assert response.context["list"] == correct_list


@pytest.mark.django_db
class TestNewList:
    def test_can_save_a_POST_request(self, client):
        response = client.post("/lists/new", data={"item_text": "A new list item"})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self, client):
        response = client.post("/lists/new", data={"item_text": "A new list item"})
        list_ = List.objects.first()
        test.assertRedirects(response, f"/lists/{list_.id}/")


@pytest.mark.django_db
class TestNewItem:
    def test_can_save_a_POST_request_to_an_existing_list(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        client.post(
            f"/lists/{correct_list.id}/add_item",
            {"item_text": "A new item for existing list"},
        )

        assert Item.objects.count() == 1

        new_item = Item.objects.first()
        assert new_item.text == "A new item for existing list"
        assert new_item.list == correct_list

    def test_redirects_to_list_view(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = client.post(
            f"/lists/{correct_list.id}/add_item",
            {"item_text": "A new item for existing list"},
        )

        test.assertRedirects(response, f"/lists/{correct_list.id}/")
