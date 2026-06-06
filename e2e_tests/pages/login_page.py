"""Page Object para la pantalla de login de SauceDemo."""

from selenium.webdriver.common.by import By

from e2e_tests.config import BASE_URL
from e2e_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self):
        return self.open(BASE_URL)

    def enter_username(self, username):
        return self.type_text(self.USERNAME_INPUT, username)

    def enter_password(self, password):
        return self.type_text(self.PASSWORD_INPUT, password)

    def submit(self):
        return self.click(self.LOGIN_BUTTON)

    def login_as(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
        return self

    def error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def is_loaded(self):
        return self.visible(self.LOGIN_BUTTON).is_displayed()
