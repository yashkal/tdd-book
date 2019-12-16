import time
import pytest
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10

@pytest.fixture
def new_browser():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()

def wait_for_row_in_list_table(browser, row_text):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id('id_list_table')
            rows = table.find_elements_by_tag_name('tr')
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)

def test_can_start_a_list_and_retrieve_it_later(new_browser, live_server):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    browser = new_browser
    browser.get(live_server.url)

    # She notices the page title and header mention to-do lists
    assert 'To-Do' in browser.title
    header_text = browser.find_element_by_tag_name('h1').text
    assert 'To-Do' in header_text

    # She is invited to enter a to-do item straight away
    input_box = browser.find_element_by_id('id_new_item')
    assert input_box.get_attribute('placeholder') == 'Enter a to-do item'

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
    input_box.send_keys('Buy peacock feathers')

    # When she hits enter, the page updates, and now the page lists
    # "1: Buy peacock feathers" as an item in a to-do list
    input_box.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, '1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
    input_box = browser.find_element_by_id('id_new_item')
    input_box.send_keys('Use peacock feathers to make a fly')
    input_box.send_keys(Keys.ENTER)

    # The page updates again, and now shows both items on her list
    wait_for_row_in_list_table(browser, '1: Buy peacock feathers')
    wait_for_row_in_list_table(browser, '2: Use peacock feathers to make a fly')

    # Satisfied, she goes back to sleep

def test_multiple_users_can_start_lists_at_different_urls(new_browser, live_server):
    # Edith starts a new to-do list
    browser = new_browser
    browser.get(live_server.url)
    inputbox = browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy peacock feathers')
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, '1: Buy peacock feathers')

    # She notices that her list has a unique URL
    edith_list_url = browser.current_url
    assert re.search(r'/lists/.+', edith_list_url)

    # Now a new user, Francis, comes along to the site
    #browser.quit()
    francis_browser = new_browser

    # There is no sign of Edith's list
    francis_browser.get(live_server.url)
    page_text = francis_browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text

    # Francis starts a new list
    inputbox = francis_browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(francis_browser, '1: Buy milk')

    # Francis gets his own url
    francis_list_url = francis_browser.current_url
    assert re.search(r'/lists/.+', edith_list_url)
    assert edith_list_url != francis_list_url

    # There is still no sign of Edith's list
    page_text = francis_browser.find_element_by_tag_name('body').text
    assert 'Buy peacock feathers' not in page_text
    assert 'make a fly' not in page_text

    # Satisfied, they both go to sleep
