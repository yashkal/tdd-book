from selenium.webdriver.common.keys import Keys

from helpers import wait_for, wait_for_row_in_list_table


def test_cannot_add_empty_list_items(new_browser):
    # Edith goes to the home page and accidently tries to submit and empty list
    # item. She hits enter on the empty input box
    browser = new_browser()
    browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

    # The home page refreshes, and there is an error message saying that list
    # items cannot be blank
    wait_for(
        lambda: browser.find_element_by_css_selector(".has-error").text,
        "You can't have an empty list item",
    )

    # She tries again, adding text this time for it to work
    browser.find_element_by_id("id_new_item").send_keys("Buy milk")
    browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")

    # Just to try again, she submits a second blank list item
    browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

    # She gets another warning on the list page
    wait_for(
        lambda: browser.find_element_by_css_selector(".has-error").text,
        "You can't have an empty list item",
    )

    # She corrects it again by filling some text in
    browser.find_element_by_id("id_new_item").send_keys("Make tea")
    browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
    wait_for_row_in_list_table(browser, "1: Buy milk")
    wait_for_row_in_list_table(browser, "2: Make tea")
