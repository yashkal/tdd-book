import pytest
from django.utils.html import escape
from lists.forms import ItemForm
from lists.models import Item, List
from pytest_django import asserts as test


class HomePageTest:
    def test_uses_home_template(self, client):
        response = client.get("/")
        test.assertTemplateUsed(response, "home.html")

    def test_home_page_uses_item_form(self, client):
        response = client.get("/")
        assert isinstance(response.context["form"], ItemForm)


@pytest.mark.django_db
class ListViewTest:
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

    def test_can_save_a_POST_request_to_an_existing_list(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        client.post(
            f"/lists/{correct_list.id}/",
            {"item_text": "A new item for existing list"},
        )

        assert Item.objects.count() == 1

        new_item = Item.objects.first()
        assert new_item.text == "A new item for existing list"
        assert new_item.list == correct_list

    def test_POST_redirects_to_list_view(self, client):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = client.post(
            f"/lists/{correct_list.id}/",
            {"item_text": "A new item for existing list"},
        )

        test.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_validation_errors_end_up_on_lists_page(self, client):
        list_ = List.objects.create()
        response = client.post(f"/lists/{list_.id}/", data={"item_text": ""})
        assert response.status_code == 200
        test.assertTemplateUsed(response, "list.html")
        expected_error = escape("You can't have an empty list item")
        test.assertContains(response, expected_error)


@pytest.mark.django_db
class NewListTest:
    def test_can_save_a_POST_request(self, client):
        response = client.post("/lists/new", data={"item_text": "A new list item"})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self, client):
        response = client.post("/lists/new", data={"item_text": "A new list item"})
        list_ = List.objects.first()
        test.assertRedirects(response, f"/lists/{list_.id}/")

    def test_validation_errors_are_sent_to_homepage_template(self, client):
        response = client.post("/lists/new", data={"item_text": ""})
        assert response.status_code == 200
        test.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        test.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self, client):
        client.post("/lists/new", data={"item_text": ""})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0
