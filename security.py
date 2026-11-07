from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from errors import ApiError
from models import Usuario

bearer = HTTPBearer(auto_error=False)


def cifrar_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def password_correcta(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def crear_token(usuario_id: int) -> str:
    vence = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expira_horas)
    return jwt.encode({"sub": str(usuario_id), "exp": vence}, settings.jwt_secret, algorithm="HS256")


def no_autenticado() -> ApiError:
    return ApiError(401, "NO_AUTENTICADO", "Tu sesión expiró, inicia sesión de nuevo")


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    if credenciales is None:
        raise no_autenticado()
    try:
        payload = jwt.decode(credenciales.credentials, settings.jwt_secret, algorithms=["HS256"])
        usuario_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise no_autenticado()

    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise no_autenticado()
    return usuario
