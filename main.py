from fastapi import FastAPI

from errors import registrar_errores
from routers import auth, canciones

app = FastAPI(title="Songs App API", version="1.0.0")
registrar_errores(app)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(canciones.router, prefix="/api/v1")
