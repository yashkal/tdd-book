def test_uses_home_template(client):
    response = client.get('/')
    assert 'home.html' in (t.name for t in response.templates)

def test_can_save_a_POST_request(client):
    response = client.post('/', data={'item_text': 'A new list item'})
    assert 'A new list item' in response.content.decode()
    assert 'home.html' in (t.name for t in response.templates)
