import pytest
from lists.models import Item

@pytest.mark.django_db
class TestHomePage:
    def test_uses_home_template(self, client):
        response = client.get('/')
        assert 'home.html' in (t.name for t in response.templates)

    def test_can_save_a_POST_request(self, client):
        response = client.post('/', data={'item_text': 'A new list item'})

        assert Item.objects.count() == 1
        new_item = Item.objects.first()
        assert new_item.text == 'A new list item'

    def test_redirects_after_POST(self, client):
        response = client.post('/', data={'item_text': 'A new list item'})

        assert response.status_code == 302
        assert response['location'] == '/'

    def test_only_saves_items_when_necessary(self, client):
        client.get('/')
        assert Item.objects.count() == 0

@pytest.mark.django_db
class TestItemModel:
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        assert saved_items.count() == 2

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        assert first_saved_item.text == 'The first (ever) list item'
        assert second_saved_item.text == 'Item the second'
