# Songs App API

API REST de Songs App, la app para llevar el repertorio de una banda. Maneja el registro, el inicio de sesión con JWT y el CRUD de canciones.

La app de Android está en [songs-app](https://github.com/manu-09-web/songs-app).

## Tecnologías

- FastAPI + Uvicorn
- MySQL 8 con SQLAlchemy 2 y PyMySQL
- JWT (PyJWT) y bcrypt
- Pydantic y pydantic-settings

## Estructura

```
main.py          arranca la API y registra los controllers
core/            configuración, conexión a MySQL, seguridad (bcrypt y JWT) y errores
models/          tablas de la base de datos (SQLAlchemy)
schemas/         datos que entran y salen, con sus validaciones (Pydantic)
repositories/    consultas a la base de datos
services/        reglas del negocio
controllers/     rutas HTTP: reciben la petición, llaman al service y responden
sql/schema.sql   script para crear la base de datos
```

## Endpoints

Base: `/api/v1`

| Método | Ruta | Token |
|---|---|---|
| POST | `/register` | No |
| POST | `/login` | No |
| GET | `/canciones` | Sí |
| GET | `/canciones/{id}` | Sí |
| POST | `/canciones` | Sí |
| PUT | `/canciones/{id}` | Sí |
| DELETE | `/canciones/{id}` | Sí |

## Cómo correrla

1. Crear la base de datos con `sql/schema.sql`.
2. Crear el entorno e instalar las librerías:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copiar `.env.example` como `.env` y poner los datos de la base de datos y la clave del token. El archivo `.env` no se sube al repositorio.
4. Arrancar la API:
   ```
   uvicorn main:app --reload --port 8000
   ```
5. Abrir `http://localhost:8000/docs` para probar los endpoints.
