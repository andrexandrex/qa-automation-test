QA Automation Challenge
=======================

Proyecto de automatizacion de pruebas para un reto tecnico de QA.

Incluye:
- Pruebas E2E con Selenium sobre SauceDemo.
- Pruebas API con requests sobre PetStore.
- Patron Page Object Model para mantener los selectores fuera de los tests.
- Reporte HTML automatico con pytest-html.
- Captura de pantalla automatica cuando falla una prueba E2E.
- Workflows de GitHub Actions para E2E y API.


Requisitos
----------

- Python 3.12 recomendado.
- Google Chrome instalado para las pruebas E2E.
- Acceso a internet para SauceDemo y PetStore.


Instalacion desde cero
----------------------

Desde la carpeta del proyecto:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

En Windows:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt


Ejecucion de pruebas
--------------------

Smoke test de Selenium:

    pytest e2e_tests/test_smoke.py

Flujo E2E completo de compra:

    pytest e2e_tests/test_purchase.py

Solo pruebas E2E:

    pytest -m e2e

Solo pruebas API:

    pytest -m api

Todas las pruebas:

    pytest

Para ejecutar Selenium sin ventana visible:

    HEADLESS=true pytest -m e2e


Reportes
--------

El proyecto genera reportes HTML automaticamente con nombre de suite y
timestamp mm-dd-hora-minuto:

    reports/e2e/e2e-report-MM-DD-HH-MM.html
    reports/api/api-report-MM-DD-HH-MM.html
    reports/all/all-report-MM-DD-HH-MM.html

Si una prueba E2E falla, tambien se guarda una captura en:

    reports/screenshots/

La carpeta reports/ no se versiona porque contiene archivos generados en
tiempo de ejecucion.


Estructura principal
--------------------

    conftest.py
        Fixture compartida de Selenium y captura de pantalla en fallo.

    pytest.ini
        Configuracion de pytest, marcadores e2e/api y reporte HTML.

    requirements.txt
        Dependencias del proyecto.

    e2e_tests/
        Pruebas de interfaz con Selenium.

    e2e_tests/pages/
        Page Objects: LoginPage, InventoryPage, CartPage y CheckoutPage.

    api_tests/
        Pruebas REST de PetStore.

    docs/
        Documentacion tecnica por fase.

    .github/workflows/
        Workflows opcionales de GitHub Actions.


Notas de depuracion
-------------------

- Si aparece "unknown marker e2e" o "unknown marker api", ejecuta pytest desde
  la raiz del proyecto, donde esta pytest.ini.
- Si aparece un error de importacion como e2e_tests.config, tambien suele ser
  porque pytest se ejecuto desde otra carpeta.
- SauceDemo usa la password publica secret_sauce. Chrome puede mostrar una
  alerta de password filtrada o insegura; esto es esperado por ser una cuenta
  demo publica.
- PetStore es una API publica de demostracion. Sus endpoints REST usan el
  prefijo /v2 aunque la pagina de documentacion sea https://petstore.swagger.io.
  Por eso el proyecto separa BASE_URL y API_PREFIX.
- Las pruebas API usan mascotas con datos unicos y reintentos en las
  verificaciones.


Comandos de checkpoint
----------------------

    pytest e2e_tests/test_smoke.py
    pytest e2e_tests/test_purchase.py
    pytest -m api

Si los tres comandos pasan, el proyecto cubre los checkpoints funcionales del
reto.
