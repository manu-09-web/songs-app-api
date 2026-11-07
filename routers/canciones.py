from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from errors import ApiError
from models import Artista, Cancion, CancionAcorde, EstadoCancion, Usuario
from schemas import CancionEntrada, CancionSalida
from security import usuario_actual

router = APIRouter(prefix="/canciones", tags=["Canciones"])


def a_salida(cancion: Cancion) -> CancionSalida:
    return CancionSalida(
        id=cancion.id,
        titulo=cancion.titulo,
        artista=cancion.artista.nombre,
        tonalidad=cancion.tonalidad,
        bpm=cancion.bpm,
        duracion_min=float(cancion.duracion_min),
        fecha_ensayo=cancion.fecha_ensayo,
        estado=cancion.estado.value,
        acordes=[a.acorde for a in cancion.acordes],
        letra=cancion.letra,
    )


def buscar_cancion(db: Session, cancion_id: int, usuario: Usuario) -> Cancion:
    cancion = db.scalar(
        select(Cancion).where(Cancion.id == cancion_id, Cancion.usuario_id == usuario.id)
    )
    if cancion is None:
        raise ApiError(404, "NO_ENCONTRADA", "La canción no existe")
    return cancion


def buscar_o_crear_artista(db: Session, nombre: str) -> Artista:
    artista = db.scalar(select(Artista).where(Artista.nombre == nombre))
    if artista is None:
        artista = Artista(nombre=nombre)
        db.add(artista)
        db.flush()
    return artista


def copiar_datos(db: Session, cancion: Cancion, datos: CancionEntrada):
    artista = buscar_o_crear_artista(db, datos.artista)
    cancion.titulo = datos.titulo
    cancion.artista = artista
    cancion.tonalidad = datos.tonalidad
    cancion.bpm = datos.bpm
    cancion.duracion_min = datos.duracion_min
    cancion.fecha_ensayo = datos.fecha_ensayo
    cancion.estado = EstadoCancion(datos.estado)
    cancion.letra = datos.letra
    # Se borran los acordes anteriores antes de insertar los nuevos,
    # porque la llave (cancion_id, posicion) no se puede repetir.
    if cancion.acordes:
        cancion.acordes.clear()
        db.flush()
    cancion.acordes = [
        CancionAcorde(posicion=i, acorde=acorde) for i, acorde in enumerate(datos.acordes, start=1)
    ]


@router.get("", response_model=list[CancionSalida])
def listar(db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_actual)):
    canciones = db.scalars(
        select(Cancion).where(Cancion.usuario_id == usuario.id).order_by(Cancion.titulo)
    ).unique()
    return [a_salida(c) for c in canciones]


@router.get("/{cancion_id}", response_model=CancionSalida)
def obtener(cancion_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_actual)):
    return a_salida(buscar_cancion(db, cancion_id, usuario))


@router.post("", response_model=CancionSalida, status_code=status.HTTP_201_CREATED)
def crear(
    datos: CancionEntrada,
    response: Response,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_actual),
):
    cancion = Cancion(usuario_id=usuario.id)
    copiar_datos(db, cancion, datos)
    db.add(cancion)
    db.commit()
    db.refresh(cancion)
    response.headers["Location"] = f"/api/v1/canciones/{cancion.id}"
    return a_salida(cancion)


@router.put("/{cancion_id}", response_model=CancionSalida)
def reemplazar(
    cancion_id: int,
    datos: CancionEntrada,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(usuario_actual),
):
    cancion = buscar_cancion(db, cancion_id, usuario)
    copiar_datos(db, cancion, datos)
    db.commit()
    db.refresh(cancion)
    return a_salida(cancion)


@router.delete("/{cancion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(cancion_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(usuario_actual)):
    cancion = buscar_cancion(db, cancion_id, usuario)
    db.delete(cancion)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
