from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from core.config import settings
from core.errors import ApiError


def cifrar_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def password_correcta(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def crear_token(usuario_id: int) -> str:
    vence = datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expira_horas)
    return jwt.encode({"sub": str(usuario_id), "exp": vence}, settings.jwt_secret, algorithm="HS256")


def no_autenticado() -> ApiError:
    return ApiError(401, "NO_AUTENTICADO", "Tu sesión expiró, inicia sesión de nuevo")


def leer_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise no_autenticado()
