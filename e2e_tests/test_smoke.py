"""Prueba de humo (smoke test).

NO es la prueba del ejercicio. Su único objetivo es confirmar que tu entorno
está bien armado: que Selenium abre el navegador, llega a SauceDemo y encuentra
el botón de login. Si esto pasa en verde, la Fase 1 está lista.

Ejecutar:  pytest e2e_tests/test_smoke.py
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from e2e_tests.config import BASE_URL, DEFAULT_TIMEOUT


@pytest.mark.e2e
def test_saucedemo_carga(driver):
    """La página de SauceDemo carga y muestra el botón de login."""
    driver.get(BASE_URL)

    login_btn = WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        EC.presence_of_element_located((By.ID, "login-button"))
    )

    assert login_btn.is_displayed(), "El botón de login no es visible"
    assert "Swag Labs" in driver.title, f"Título inesperado: {driver.title}"
