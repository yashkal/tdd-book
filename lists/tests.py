import pytest
from lists.models import Item

def test_uses_home_template(client):
    response = client.get('/')
    assert 'home.html' in (t.name for t in response.templates)

def test_can_save_a_POST_request(client):
    response = client.post('/', data={'item_text': 'A new list item'})
    assert 'A new list item' in response.content.decode()
    assert 'home.html' in (t.name for t in response.templates)

@pytest.mark.django_db
def test_saving_and_retrieving_items():
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
