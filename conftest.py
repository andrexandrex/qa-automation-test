"""Configuración compartida de pytest (fixtures y hooks).

Este archivo lo carga pytest automáticamente. Aquí vive:
  1. La fixture `driver`: entrega un navegador limpio a cada prueba E2E
     y lo cierra al terminar (pase o falle).
  2. Un hook que guarda una captura de pantalla cuando una prueba E2E falla,
     muy útil para depurar.
"""

import os
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Carpeta donde se guardan las capturas de fallos
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")


@pytest.fixture
def driver():
    """Entrega un navegador Chrome listo para usar.

    - Selenium >= 4.6 descarga el driver solo (Selenium Manager); no hace
      falta instalar chromedriver a mano.
    - Para correr SIN ventana visible (CI o servidores), exportar:
          HEADLESS=true
    """
    options = Options()
    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    drv = webdriver.Chrome(options=options)
    # Usamos SOLO esperas explícitas (WebDriverWait), por eso el implícito en 0.
    drv.implicitly_wait(0)

    yield drv

    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Si una prueba con `driver` falla, guarda una captura de pantalla."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(SCREENSHOTS_DIR, f"{item.name}_{stamp}.png")
            drv.save_screenshot(path)
            print(f"\n[captura guardada] {path}")
