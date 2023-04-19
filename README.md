# Fapro Test

Este repositorio contiene una API desarrollada en Python usando Flask, requests, y BeautifulSoup4 para recuperar el valor de la Unidad de Fomento (UF) para una fecha específica. La API permite a los usuarios consultar el valor de la UF para cualquier fecha mayor al 01-01-2013.

## Requerimientos

- Python 3.8+
- Flask
- requests
- beautifulsoup4
- pytest

## Uso

Para usar la API, clone el repositorio e instale las dependencias. Luego, inicie el servidor Flask ejecutando el siguiente comando:

```bash
$ flask run
```

La API expone un endpoint(**/api/date**) que acepta solicitudes GET y POST:

**Con la fecha como parámetro URL o como parámetro de cuerpo en formato JSON.**

El formato del parámetro fecha es **DD-MM-YYYY.**

### GET `/api/date`

Parámetros de consulta:

- `date`: la fecha para la cual se debe recuperar el valor de la UF. Debe estar en el formato `DD-MM-YYYY`.

Ejemplo:

```bash
$ curl http://127.0.0.1:5000/api/date?date=01-02-2015
```

### POST `/api/date`

Cuerpo:

- `date`: la fecha para la cual se debe recuperar el valor de la UF. Debe estar en el formato `DD-MM-YYYY`.

Ejemplo:

```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"date": "01-02-2015"}' http://127.0.0.1:5000/api/date
```

Ejemplo de respuesta satisfactoria:

```bash
{
  "UF": 23786.62
}
```

Si la fecha falta, o si no está en el formato correcto, o si no está dentro del rango permitido, entonces la API devolverá un mensaje de error en formato JSON:

```json
{
  "error": "DATE_MISSING",
  "message": "Date is a required parameter."
}

{
  "error": "DATE_INVALID_FORMAT",
  "message": "Date format must be DD-MM-YYYY."
}
{
  "error": "DATE_INVALID_RANGE",
  "message": "Date must be greater than 01-01-2013 and less than today."
}
```

Si hay un error de red al intentar recuperar el valor de la UF, entonces la API devolverá un mensaje de error en formato JSON:

```json
{
  "error": "CONNECTION_ERROR",
  "message": "Unable to retrieve UF value due to a network error."
}
```

## Pruebas

Para ejecutar las pruebas unitarias, instale la biblioteca `pytest` y ejecute el siguiente comando:

```bash
$ pytest
```

Las pruebas garantizan que la API devuelva las respuestas esperadas para entradas válidas e inválidas.