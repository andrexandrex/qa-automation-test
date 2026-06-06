Pruebas E2E - SauceDemo
=======================

Este archivo explica como ejecutar las pruebas end-to-end de interfaz. Las
pruebas usan Selenium con Chrome para automatizar SauceDemo y validar que el
flujo de compra principal termina con el mensaje de confirmacion esperado.


Requisitos
----------

- Python 3.12 recomendado.
- Google Chrome instalado.
- Acceso a internet.
- Dependencias instaladas desde requirements.txt.


Instalacion
-----------

Desde la raiz del proyecto:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

En Windows:

    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt


Ejecucion
---------

Para comprobar que Selenium abre Chrome y carga SauceDemo:

    pytest e2e_tests/test_smoke.py

Para correr el flujo completo de compra:

    pytest e2e_tests/test_purchase.py

Para correr todas las pruebas E2E:

    pytest -m e2e

Para ejecutar sin ventana visible, util para CI:

    HEADLESS=true pytest -m e2e


Que valida la prueba de compra
------------------------------

La prueba inicia sesion con el usuario demo, agrega el producto Sauce Labs
Backpack al carrito, abre el carrito, completa el checkout, finaliza la compra
y valida que aparezca el mensaje:

    THANK YOU FOR YOUR ORDER!

La automatizacion usa Page Object Model. Esto significa que los selectores y
acciones de cada pantalla viven en clases como LoginPage, InventoryPage,
CartPage y CheckoutPage. El test queda enfocado en el flujo del usuario y no en
los detalles de Selenium.


Reportes y evidencias
---------------------

Cada ejecucion E2E genera un reporte HTML con timestamp en:

    reports/e2e/

El nombre sigue este formato:

    e2e-report-MM-DD-HH-MM.html

Si una prueba E2E falla, el proyecto guarda automaticamente una captura en:

    reports/screenshots/


Notas utiles
------------

SauceDemo usa credenciales publicas de demostracion. Chrome puede mostrar una
advertencia relacionada con la password secret_sauce porque es una password
conocida. Para este ejercicio no se considera un defecto del flujo.

Algunas zonas del checkout tienen comportamiento sensible al tamano de ventana
y a la posicion del footer. Por eso el navegador se abre con un tamano fijo y
las acciones mas delicadas estan encapsuladas dentro de los Page Objects.
