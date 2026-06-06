Pruebas API - PetStore
======================

Este archivo explica como ejecutar las pruebas de servicio REST incluidas en el
proyecto. Las pruebas usan la API publica de PetStore para validar el flujo de
una mascota: crearla, consultarla por ID, actualizar su nombre y estado, y
confirmar que aparece al buscar por estatus.


Requisitos
----------

- Python 3.12 recomendado.
- Acceso a internet.
- Dependencias instaladas desde requirements.txt.

PetStore publica su documentacion en:

    https://petstore.swagger.io

Los endpoints REST usados por la prueba trabajan bajo el prefijo:

    /v2

Por eso la configuracion separa la URL base del prefijo de API. La URL base
representa el sitio/documentacion y el prefijo representa la version real de
los endpoints.


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

Para correr solamente las pruebas API:

    pytest -m api

Tambien se puede ejecutar directamente el archivo:

    pytest api_tests/test_pet_crud.py


Que valida la prueba
--------------------

La prueba genera una mascota con datos unicos para evitar choques con otras
ejecuciones de la API publica. Luego realiza estos pasos:

1. Agrega una mascota a la tienda.
2. Consulta la mascota ingresada previamente por ID.
3. Actualiza el nombre de la mascota y cambia su estatus a sold.
4. Consulta las mascotas por estatus sold y confirma que la mascota actualizada
   aparece en la respuesta.


Reportes
--------

Cada ejecucion genera un reporte HTML con timestamp en:

    reports/api/

El nombre sigue este formato:

    api-report-MM-DD-HH-MM.html

Si se ejecuta mas de una vez en el mismo minuto, pytest agrega un sufijo para
no sobrescribir el reporte anterior.


Notas utiles
------------

PetStore es un servicio publico de demostracion. A veces puede tardar unos
segundos en reflejar un alta o una actualizacion. Por eso la prueba no repite
la accion principal; repite solo las verificaciones hasta que el servicio
devuelve el dato esperado o hasta agotar los intentos configurados.
