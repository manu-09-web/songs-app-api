from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    def __init__(self, status: int, codigo: str, mensaje: str):
        self.status = status
        self.codigo = codigo
        self.mensaje = mensaje


def respuesta_error(status: int, codigo: str, mensaje: str, detalles=None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"codigo": codigo, "mensaje": mensaje, "detalles": detalles},
    )


def mensaje_validacion(error: dict) -> str:
    if error["type"] == "value_error":
        return str(error["ctx"]["error"])
    if error["type"] == "missing":
        return "Campo obligatorio"
    return "Valor no válido"


def registrar_errores(app: FastAPI):
    @app.exception_handler(ApiError)
    async def error_api(request: Request, exc: ApiError):
        return respuesta_error(exc.status, exc.codigo, exc.mensaje)

    @app.exception_handler(RequestValidationError)
    async def error_validacion(request: Request, exc: RequestValidationError):
        detalles = []
        for error in exc.errors():
            loc = [str(parte) for parte in error["loc"] if parte != "body"]
            campo = loc[0] if loc else "body"
            if not any(d["campo"] == campo for d in detalles):
                detalles.append({"campo": campo, "mensaje": mensaje_validacion(error)})
        return respuesta_error(422, "VALIDACION", "Hay campos con errores", detalles)

    @app.exception_handler(StarletteHTTPException)
    async def error_http(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            return respuesta_error(404, "NO_ENCONTRADA", "La ruta no existe")
        return respuesta_error(exc.status_code, "ERROR_HTTP", str(exc.detail))

    @app.exception_handler(Exception)
    async def error_interno(request: Request, exc: Exception):
        return respuesta_error(500, "ERROR_INTERNO", "El servidor tuvo un problema, intenta más tarde")
