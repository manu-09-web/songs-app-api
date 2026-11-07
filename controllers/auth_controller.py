from fastapi import APIRouter, Depends, status

from core.dependencies import auth_service
from schemas.auth import AuthRespuesta, LoginEntrada, RegistroEntrada
from services.auth_service import AuthService

router = APIRouter(tags=["Autenticación"])


@router.post("/register", response_model=AuthRespuesta, status_code=status.HTTP_201_CREATED)
def registrar(datos: RegistroEntrada, service: AuthService = Depends(auth_service)):
    return service.registrar(datos)


@router.post("/login", response_model=AuthRespuesta)
def iniciar_sesion(datos: LoginEntrada, service: AuthService = Depends(auth_service)):
    return service.iniciar_sesion(datos)
