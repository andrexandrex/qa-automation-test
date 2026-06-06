"""Page Object para las pantallas de checkout de SauceDemo."""

from selenium.webdriver.common.by import By

from e2e_tests.pages.base_page import BasePage


class CheckoutPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    CHECKOUT_SUMMARY = (By.CLASS_NAME, "checkout_summary_container")
    SUMMARY_ITEMS = (By.CLASS_NAME, "cart_item")
    SUMMARY_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    FINISH_BUTTON = (By.ID, "finish")

    COMPLETE_CONTAINER = (By.ID, "checkout_complete_container")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def is_information_step_loaded(self):
        return self.visible(self.FIRST_NAME_INPUT).is_displayed()

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def fill_information(self, first_name, last_name, postal_code):
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def continue_to_overview(self):
        return self.js_click(self.CONTINUE_BUTTON)

    def cancel(self):
        return self.js_click(self.CANCEL_BUTTON)

    def error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_overview_step_loaded(self):
        return self.visible(self.CHECKOUT_SUMMARY).is_displayed()

    def summary_item_names(self):
        return [item.text for item in self.find_all(self.SUMMARY_ITEM_NAMES)]

    def finish(self):
        return self.js_click(self.FINISH_BUTTON)

    def is_complete_step_loaded(self):
        return self.visible(self.COMPLETE_CONTAINER).is_displayed()

    def complete_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def back_home(self):
        return self.js_click(self.BACK_HOME_BUTTON)
