import pytest
from selenium.webdriver.common.keys import Keys

from helpers import get_item_input_box, wait_for_row_in_list_table


def test_layout_and_styling(new_browser):
    browser = new_browser()
    browser.set_window_size(1024, 768)

    # She notices the input box is nicely centered
    inputbox = get_item_input_box(browser)
    assert (
        pytest.approx(512, abs=10)
        == inputbox.location["x"] + inputbox.size["width"] / 2
    )

    # She starts a new list and sees the input is nicely
    # centered there too
    inputbox.send_keys("testing")
    inputbox.send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: testing")
    inputbox = get_item_input_box(browser)
    assert (
        pytest.approx(512, abs=10)
        == inputbox.location["x"] + inputbox.size["width"] / 2
    )
