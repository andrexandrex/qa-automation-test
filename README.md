# QA Automation Challenge

[![API Tests](https://github.com/andrexandrex/qa-automation-test/actions/workflows/api.yml/badge.svg)](https://github.com/andrexandrex/qa-automation-test/actions/workflows/api.yml)
[![E2E Tests](https://github.com/andrexandrex/qa-automation-test/actions/workflows/e2e.yml/badge.svg)](https://github.com/andrexandrex/qa-automation-test/actions/workflows/e2e.yml)

Proyecto de automatización de pruebas con Python, pytest, Selenium y requests.
Incluye pruebas E2E para SauceDemo y pruebas API para PetStore.

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución Local

Smoke test de Selenium:

```bash
pytest e2e_tests/test_smoke.py
```

Flujo E2E completo:

```bash
pytest -m e2e
```

Pruebas API:

```bash
pytest -m api
```

Todas las pruebas:

```bash
HEADLESS=true pytest
```

## Reportes Locales

Los reportes HTML se generan automáticamente con timestamp:

- `reports/e2e/e2e-report-MM-DD-HH-MM.html`
- `reports/api/api-report-MM-DD-HH-MM.html`
- `reports/all/all-report-MM-DD-HH-MM.html`

Si una prueba E2E falla, se guarda una captura en `reports/screenshots/`.

## Reportes En GitHub Actions

Los workflows suben los reportes como artefactos descargables:

1. Entra al repositorio en GitHub.
2. Abre la pestaña `Actions`.
3. Selecciona `API Tests` o `E2E Tests`.
4. Abre la ejecución que quieras revisar.
5. Baja hasta `Artifacts`.
6. Descarga `api-reports-<run_number>` o `e2e-reports-<run_number>`.
7. Descomprime el archivo y abre el `.html` del reporte.

Los badges de arriba muestran si la última ejecución de cada workflow pasó o
falló. El reporte HTML no se puede mostrar directamente dentro del README como
archivo dinámico porque GitHub Actions genera artefactos por ejecución. Para
tener un enlace público y estable al último reporte, configura GitHub Pages y
publica los reportes desde el workflow.

Configuración sugerida para GitHub Pages:

1. En GitHub, ve a `Settings > Pages`.
2. En `Build and deployment`, selecciona `GitHub Actions`.
3. Agrega permisos `pages: write` e `id-token: write` al workflow que quieras
   publicar.
4. Después de correr pytest, usa `actions/upload-pages-artifact` con la carpeta
   `reports/`.
5. Agrega un job con `actions/deploy-pages`.
6. Cuando Pages quede activo, puedes añadir al README un enlace como:

```markdown
[Último reporte publicado](https://andrexandrex.github.io/qa-automation-test/)
```

Para esta entrega, los reportes ya quedan disponibles como artefactos de cada
ejecución de CI, que es la forma más simple y segura para revisión.

## Documentos De Entrega

- `readme_e2e.txt`: instrucciones específicas para pruebas E2E.
- `conclusiones_e2e.txt`: hallazgos y conclusiones E2E.
- `readme_api.txt`: instrucciones específicas para pruebas API.
- `conclusiones_api.txt`: hallazgos y conclusiones API.
