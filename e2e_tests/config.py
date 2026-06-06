"""Configuración centralizada de las pruebas E2E.

Mantener URLs y credenciales aquí (y NO repartidas por el código) es una
buena práctica: si la URL cambia, se edita en un solo lugar.
"""

BASE_URL = "https://www.saucedemo.com/"

# Credenciales provistas por el ejercicio
STANDARD_USER = "standard_user"
PASSWORD = "secret_sauce"

# Tiempo máximo (segundos) que esperan los waits explícitos antes de fallar
DEFAULT_TIMEOUT = 10
