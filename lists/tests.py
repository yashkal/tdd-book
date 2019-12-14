def test_uses_home_template(client):
    response = client.get('/')
    assert 'home.html' in (t.name for t in response.templates)
