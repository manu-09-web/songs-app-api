from fastapi import APIRouter, Depends, Response, status

from core.dependencies import cancion_service, usuario_actual
from models import Usuario
from schemas.cancion import CancionEntrada, CancionSalida
from services.cancion_service import CancionService

router = APIRouter(prefix="/canciones", tags=["Canciones"])


@router.get("", response_model=list[CancionSalida])
def listar(
    service: CancionService = Depends(cancion_service),
    usuario: Usuario = Depends(usuario_actual),
):
    return service.listar(usuario)


@router.get("/{cancion_id}", response_model=CancionSalida)
def obtener(
    cancion_id: int,
    service: CancionService = Depends(cancion_service),
    usuario: Usuario = Depends(usuario_actual),
):
    return service.obtener(cancion_id, usuario)


@router.post("", response_model=CancionSalida, status_code=status.HTTP_201_CREATED)
def crear(
    datos: CancionEntrada,
    response: Response,
    service: CancionService = Depends(cancion_service),
    usuario: Usuario = Depends(usuario_actual),
):
    cancion = service.crear(datos, usuario)
    response.headers["Location"] = f"/api/v1/canciones/{cancion.id}"
    return cancion


@router.put("/{cancion_id}", response_model=CancionSalida)
def reemplazar(
    cancion_id: int,
    datos: CancionEntrada,
    service: CancionService = Depends(cancion_service),
    usuario: Usuario = Depends(usuario_actual),
):
    return service.reemplazar(cancion_id, datos, usuario)


@router.delete("/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    cancion_id: int,
    service: CancionService = Depends(cancion_service),
    usuario: Usuario = Depends(usuario_actual),
):
    service.eliminar(cancion_id, usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
