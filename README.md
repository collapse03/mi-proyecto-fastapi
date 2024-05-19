# Mi Proyecto FastAPI

Este proyecto de ejemplo tiene como objetivo realizar un login de un usuario registrador por username unico creado en una base de datos no relacional. Se utiliza un hash para la contraseña con la ayuda de una libreria de Python.

## Instalación

Para instalar las dependencias del proyecto, ejecute el siguiente comando:

```
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la aplicación, use el siguiente comando:

```
uvicorn app.main:app --reload
```

Esto iniciará el servidor en `http://localhost:8000`.

## Pruebas

Para ejecutar las pruebas, use el siguiente comando:

```
pytest
```
```