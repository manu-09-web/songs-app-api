from fastapi import FastAPI

from controllers import auth_controller, cancion_controller
from core.errors import registrar_errores

app = FastAPI(title="Songs App API", version="1.0.0")
registrar_errores(app)

app.include_router(auth_controller.router, prefix="/api/v1")
app.include_router(cancion_controller.router, prefix="/api/v1")
