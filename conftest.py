"""Configuración compartida de pytest (fixtures y hooks).

Este archivo lo carga pytest automáticamente. Aquí vive:
  1. La fixture `driver`: entrega un navegador limpio a cada prueba E2E
     y lo cierra al terminar (pase o falle).
  2. Un hook que guarda una captura de pantalla cuando una prueba E2E falla,
     muy útil para depurar.
"""

import os
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Carpeta donde se guardan las capturas de fallos
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
REPORTS_DIR = Path(__file__).parent / "reports"


def _report_category(config):
    markexpr = (getattr(config.option, "markexpr", "") or "").lower()
    args = " ".join(str(arg).lower() for arg in config.args)

    if "api" in markexpr or "api_tests" in args:
        return "api"
    if "e2e" in markexpr or "e2e_tests" in args:
        return "e2e"
    return "all"


def _unique_report_path(category):
    stamp = datetime.now().strftime("%m-%d-%H-%M")
    report_dir = REPORTS_DIR / category
    report_dir.mkdir(parents=True, exist_ok=True)

    path = report_dir / f"{category}-report-{stamp}.html"
    counter = 2
    while path.exists():
        path = report_dir / f"{category}-report-{stamp}-{counter}.html"
        counter += 1
    return path


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Genera reportes HTML con nombre segun suite y timestamp."""
    if not config.pluginmanager.hasplugin("html"):
        return
    if config.getoption("htmlpath"):
        return

    category = _report_category(config)
    config.option.htmlpath = str(_unique_report_path(category))
    config.option.self_contained_html = True


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
