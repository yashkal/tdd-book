import os

import pytest
from selenium import webdriver


@pytest.fixture
def new_browser(request):
    def _new_browser():
        browser = webdriver.Firefox()
        request.addfinalizer(lambda b=browser: b.quit())
        browser.get(os.environ.get("STAGING_ENVIRONMENT"))
        return browser

    yield _new_browser
