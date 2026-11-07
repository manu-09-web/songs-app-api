from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from errors import ApiError
from models import Usuario
from schemas import AuthRespuesta, LoginEntrada, RegistroEntrada, UsuarioSalida
from security import cifrar_password, crear_token, password_correcta

router = APIRouter(tags=["Autenticación"])


def respuesta_sesion(usuario: Usuario) -> AuthRespuesta:
    return AuthRespuesta(
        access_token=crear_token(usuario.id),
        usuario=UsuarioSalida.model_validate(usuario),
    )


@router.post("/register", response_model=AuthRespuesta, status_code=status.HTTP_201_CREATED)
def registrar(datos: RegistroEntrada, db: Session = Depends(get_db)):
    if db.scalar(select(Usuario).where(Usuario.email == datos.email)):
        raise ApiError(409, "EMAIL_EN_USO", "Ese correo ya está registrado")

    usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        password_hash=cifrar_password(datos.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return respuesta_sesion(usuario)


@router.post("/login", response_model=AuthRespuesta)
def iniciar_sesion(datos: LoginEntrada, db: Session = Depends(get_db)):
    usuario = db.scalar(select(Usuario).where(Usuario.email == datos.email))
    if usuario is None or not password_correcta(datos.password, usuario.password_hash):
        raise ApiError(401, "CREDENCIALES_INVALIDAS", "Correo o contraseña incorrectos")
    return respuesta_sesion(usuario)
