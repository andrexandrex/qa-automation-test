"""Prueba E2E del flujo de compra completo en SauceDemo."""

import pytest

from e2e_tests.config import PASSWORD, STANDARD_USER
from e2e_tests.pages import CartPage, CheckoutPage, InventoryPage, LoginPage


@pytest.mark.e2e
def test_complete_purchase_flow(driver):
    product_name = "Sauce Labs Backpack"

    LoginPage(driver).load().login_as(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    inventory_page.add_product_to_cart(product_name)
    inventory_page.open_cart()

    cart_page = CartPage(driver)
    cart_page.checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.fill_information("QA", "Automation", "15001")
    checkout_page.continue_to_overview()
    checkout_page.finish()

    assert (
        checkout_page.complete_message().upper() == "THANK YOU FOR YOUR ORDER!"
    )
