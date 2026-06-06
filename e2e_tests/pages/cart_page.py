"""Page Object para el carrito de compras de SauceDemo."""

from selenium.webdriver.common.by import By

from e2e_tests.pages.base_page import BasePage


class CartPage(BasePage):
    PAGE_TITLE = (By.CLASS_NAME, "title")
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")

    def is_loaded(self):
        return self.visible(self.CART_LIST).is_displayed()

    def title(self):
        return self.get_text(self.PAGE_TITLE)

    def item_names(self):
        return [item.text for item in self.find_all(self.ITEM_NAMES)]

    def remove_product(self, product_name):
        self.js_click(self._remove_button(product_name))
        return self

    def continue_shopping(self):
        self.js_click(self.CONTINUE_SHOPPING_BUTTON)
        self.wait_for_url_contains("inventory.html")
        return self

    def checkout(self):
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("checkout-step-one.html")
        return self

    def _remove_button(self, product_name):
        product = self.xpath_literal(product_name)
        return (
            By.XPATH,
            "//div[contains(@class, 'cart_item')]"
            f"[.//div[contains(@class, 'inventory_item_name') and normalize-space()={product}]]"
            "//button[starts-with(@id, 'remove')]",
        )
