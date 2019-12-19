import pytest
from django.test import SimpleTestCase

from lists.models import Item


@pytest.mark.django_db
class TestHomePage:
    def test_uses_home_template(self, client):
        response = client.get("/")
        SimpleTestCase().assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self, client):
        response = client.post("/", data={"item_text": "A new list item"})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self, client):
        response = client.post("/", data={"item_text": "A new list item"})

        SimpleTestCase().assertRedirects(response, "/lists/the-only-list/")

    def test_only_saves_items_when_necessary(self, client):
        client.get("/")
        assert Item.objects.count() == 0


@pytest.mark.django_db
class TestItemModel:
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        assert saved_items.count() == 2

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        assert first_saved_item.text == "The first (ever) list item"
        assert second_saved_item.text == "Item the second"


@pytest.mark.django_db
class TestListView:
    def test_uses_list_template(self, client):
        response = client.get("/lists/the-only-list/")
        SimpleTestCase().assertTemplateUsed(response, "list.html")

    def test_displays_all_list_items(self, client):
        Item.objects.create(text="itemey 1")
        Item.objects.create(text="itemey 2")

        response = client.get("/lists/the-only-list/")

        assert response.status_code == 200
        assert "itemey 1" in response.content.decode()
        assert "itemey 2" in response.content.decode()
