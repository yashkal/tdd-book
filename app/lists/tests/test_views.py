import pytest
from django.utils.html import escape
from lists.forms import EMPTY_ITEM_ERROR, ExistingListItemForm, ItemForm
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
            {"text": "A new item for existing list"},
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
            {"text": "A new item for existing list"},
        )

        test.assertRedirects(response, f"/lists/{correct_list.id}/")

    def test_displays_item_form(self, client):
        list_ = List.objects.create()
        response = client.get(f"/lists/{list_.id}/")
        assert isinstance(response.context["form"], ExistingListItemForm)
        test.assertContains(response, 'name="text"')

    @pytest.fixture()
    def post_invalid_input(self, client):
        list_ = List.objects.create()
        return client.post(f"/lists/{list_.id}/", data={"text": ""})

    def test_invalid_input_doesnt_save_to_db(self, post_invalid_input):
        assert Item.objects.count() == 0

    def test_invalid_input_renders_list_template(self, post_invalid_input):
        response = post_invalid_input
        assert response.status_code == 200
        test.assertTemplateUsed(response, "list.html")

    def test_invalid_input_passes_form_to_template(self, post_invalid_input):
        response = post_invalid_input
        assert isinstance(response.context["form"], ExistingListItemForm)

    def test_invalid_input_shows_error_on_page(self, post_invalid_input):
        response = post_invalid_input
        test.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_show_up_on_lists_page(self, client):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text="textey")
        response = client.post(f"/lists/{list1.id}/", data={"text": "textey"})

        expected_error = escape("You've already got this in your list")
        test.assertContains(response, expected_error)
        test.assertTemplateUsed(response, "list.html")
        assert Item.objects.all().count() == 1


@pytest.mark.django_db
class NewListTest:
    def test_can_save_a_POST_request(self, client):
        response = client.post("/lists/new", data={"text": "A new list item"})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == "A new list item"

    def test_redirects_after_POST(self, client):
        response = client.post("/lists/new", data={"text": "A new list item"})
        list_ = List.objects.first()
        test.assertRedirects(response, f"/lists/{list_.id}/")

    def test_invalid_input_renders_home_page_template(self, client):
        response = client.post("/lists/new", data={"text": ""})
        assert response.status_code == 200
        test.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self, client):
        response = client.post("/lists/new", data={"text": ""})
        test.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_invalid_input_passes_form_to_template(self, client):
        response = client.post("/lists/new", data={"text": ""})
        assert isinstance(response.context["form"], ItemForm)

    def test_invalid_list_items_arent_saved(self, client):
        client.post("/lists/new", data={"text": ""})
        assert List.objects.count() == 0
        assert Item.objects.count() == 0
