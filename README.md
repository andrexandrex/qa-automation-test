# QA Automation Challenge

Proyecto de automatización de pruebas para el reto técnico:

- **E2E (Selenium + Python):** flujo de compra en [SauceDemo](https://www.saucedemo.com/).
- **API (requests + Python):** CRUD de usuario en [PetStore](https://petstore.swagger.io/).

> Repositorio en construcción por fases. La Fase 1 valida que Selenium pueda
> abrir Chrome y cargar SauceDemo correctamente.

## Estructura

```
qa-automation-challenge/
├── conftest.py          # fixtures compartidas (driver, captura en fallo)
├── pytest.ini           # marcadores: -m e2e / -m api
├── requirements.txt
├── e2e_tests/           # pruebas de interfaz (Selenium)
│   ├── config.py
│   ├── pages/           # Page Object Model (Fase 2)
│   └── test_smoke.py    # verificación de entorno (Fase 1)
└── api_tests/           # pruebas REST (Fase 4)
    └── config.py
```

## Puesta en marcha rápida

```bash
cd qa-automation-challenge
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
pytest e2e_tests/test_smoke.py  # debe abrir Chrome y pasar en verde
```

Notas de depuración:

- Si aparece `unknown marker e2e`, ejecuta `pytest` desde la carpeta que contiene `pytest.ini`.
- Si aparece un error de importación como `e2e_tests.config`, ejecuta `pytest` desde la raíz del proyecto.
- Para ejecutar sin ventana visible, usa `HEADLESS=true pytest e2e_tests/test_smoke.py`.
