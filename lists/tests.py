from lists.views import home_page

def test_home_page_returns_correct_html(client):
    response = client.get('/')

    html = response.content.decode('utf8')
    assert '<html>' in html
    assert '<title>To-Do lists</title>' in html
    assert html.strip().endswith('</html>')

    assert 'home.html' in (t.name for t in response.templates)
