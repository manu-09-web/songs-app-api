from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Cancion, CancionAcorde


class CancionRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_de_usuario(self, usuario_id: int) -> list[Cancion]:
        consulta = select(Cancion).where(Cancion.usuario_id == usuario_id).order_by(Cancion.titulo)
        return list(self.db.scalars(consulta).unique())

    def buscar_de_usuario(self, cancion_id: int, usuario_id: int) -> Cancion | None:
        return self.db.scalar(
            select(Cancion).where(Cancion.id == cancion_id, Cancion.usuario_id == usuario_id)
        )

    def reemplazar_acordes(self, cancion: Cancion, acordes: list[str]):
        # Se borran los acordes anteriores antes de insertar los nuevos,
        # porque la llave (cancion_id, posicion) no se puede repetir.
        if cancion.acordes:
            cancion.acordes.clear()
            self.db.flush()
        cancion.acordes = [
            CancionAcorde(posicion=i, acorde=acorde) for i, acorde in enumerate(acordes, start=1)
        ]

    def guardar(self, cancion: Cancion) -> Cancion:
        self.db.add(cancion)
        self.db.commit()
        self.db.refresh(cancion)
        return cancion

    def eliminar(self, cancion: Cancion):
        self.db.delete(cancion)
        self.db.commit()
