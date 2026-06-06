"""Utilidades comunes para los Page Objects de Selenium."""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from e2e_tests.config import DEFAULT_TIMEOUT


class BasePage:
    """Base mínima con acciones y esperas explícitas reutilizables."""

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        return self

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        self.clickable(locator).click()
        return self

    def type_text(self, locator, text):
        element = self.visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        element.click()
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator):
        return self.visible(locator).text

    def wait_for_url_contains(self, partial_url):
        return self.wait.until(EC.url_contains(partial_url))

    @staticmethod
    def xpath_literal(value):
        """Escapa strings para usarlos de forma segura en XPath."""
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"
