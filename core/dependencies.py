from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import leer_token, no_autenticado
from models import Usuario
from repositories.artista_repository import ArtistaRepository
from repositories.cancion_repository import CancionRepository
from repositories.usuario_repository import UsuarioRepository
from services.auth_service import AuthService
from services.cancion_service import CancionService

bearer = HTTPBearer(auto_error=False)


def auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UsuarioRepository(db))


def cancion_service(db: Session = Depends(get_db)) -> CancionService:
    return CancionService(CancionRepository(db), ArtistaRepository(db))


def usuario_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    if credenciales is None:
        raise no_autenticado()
    usuario = UsuarioRepository(db).buscar_por_id(leer_token(credenciales.credentials))
    if usuario is None:
        raise no_autenticado()
    return usuario
