"""Configuración centralizada de las pruebas de API (PetStore)."""

import os

BASE_URL = "https://petstore.swagger.io"
API_PREFIX = "/v2"
API_BASE_URL = os.getenv("PETSTORE_API_BASE_URL", f"{BASE_URL}{API_PREFIX}")

# Tiempo máximo (segundos) de espera por respuesta del servicio
DEFAULT_TIMEOUT = 10
