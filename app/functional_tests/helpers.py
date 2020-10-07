import time

from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


def wait_for(fn, row_text):
    start_time = time.time()
    while True:
        try:
            assert fn() == row_text
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)


def wait_for_row_in_list_table(browser, row_text):
    start_time = time.time()
    while True:
        try:
            table = browser.find_element_by_id("id_list_table")
            rows = table.find_elements_by_tag_name("tr")
            assert row_text in [row.text for row in rows]
            return
        except (AssertionError, WebDriverException) as e:
            if time.time() - start_time > MAX_WAIT:
                raise e
            time.sleep(0.5)
