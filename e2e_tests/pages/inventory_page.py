"""Page Object para el inventario de productos de SauceDemo."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from e2e_tests.pages.base_page import BasePage


class InventoryPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def is_loaded(self):
        return self.visible(self.INVENTORY_CONTAINER).is_displayed()

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def product_names(self):
        return [item.text for item in self.find_all(self.ITEM_NAMES)]

    def sort_by(self, visible_text):
        Select(self.visible(self.SORT_DROPDOWN)).select_by_visible_text(visible_text)
        return self

    def add_product_to_cart(self, product_name):
        self.js_click(self._product_button(product_name, "Add to cart"))
        self.visible(self._product_button(product_name, "Remove"))
        return self

    def remove_product_from_cart(self, product_name):
        self.js_click(self._product_button(product_name, "Remove"))
        self.visible(self._product_button(product_name, "Add to cart"))
        return self

    def open_cart(self):
        self.js_click(self.SHOPPING_CART_LINK)
        self.wait_for_url_contains("cart.html")
        return self

    def cart_badge_count(self):
        return int(self.get_text(self.CART_BADGE))

    def _product_button(self, product_name, button_text):
        product = self.xpath_literal(product_name)
        button = self.xpath_literal(button_text)
        return (
            By.XPATH,
            "//div[contains(@class, 'inventory_item')]"
            f"[.//div[contains(@class, 'inventory_item_name') and normalize-space()={product}]]"
            f"//button[normalize-space()={button}]",
        )
