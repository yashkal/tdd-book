from selenium.webdriver.common.keys import Keys

from helpers import get_item_input_box, wait_for, wait_for_row_in_list_table


def get_error_element(browser):
    return browser.find_element_by_css_selector(".has-error")


def test_cannot_add_empty_list_items(new_browser):
    # Edith goes to the home page and accidently tries to submit and empty list
    # item. She hits enter on the empty input box
    browser = new_browser()
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # Browser intercepts the request, and does not load the list page
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:invalid"))

    # She starts writing text for the new item and the error disappears
    get_item_input_box(browser).send_keys("Buy milk")
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:valid"))

    # And she can submit successfully
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Perversely, she submits a second blank list item
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # Again, the browser will not comply
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:invalid"))

    # She can correct it by filling some text in
    get_item_input_box(browser).send_keys("Make tea")
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:valid"))
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for_row_in_list_table(browser, "2: Make tea")


def test_cannot_add_duplicate_items(new_browser):
    # Edith goes to the homepage and starts a new list
    browser = new_browser()
    get_item_input_box(browser).send_keys("Buy wellies")
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy wellies")

    # She accidently tries to add a duplicate item
    get_item_input_box(browser).send_keys("Buy wellies")
    get_item_input_box(browser).send_keys(Keys.ENTER)

    # She sees a helpful error message
    assert (
        wait_for(lambda: get_error_element(browser).text)
        == "You've already got this in your list"
    )


def test_error_messages_are_cleared_on_input(new_browser):
    browser = new_browser()

    # Edith starts a new list and causes a validation error
    get_item_input_box(browser).send_keys("Banter too thick")
    get_item_input_box(browser).send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Banter too thick")
    get_item_input_box(browser).send_keys("Banter too thick")
    get_item_input_box(browser).send_keys(Keys.ENTER)

    assert wait_for(lambda: get_error_element(browser).is_displayed())

    # She starts typing in the input box to clear the error
    get_item_input_box(browser).send_keys("a")

    # She is pleased to see the error message disappear
    assert wait_for(lambda: get_error_element(browser).is_displayed()) is False
