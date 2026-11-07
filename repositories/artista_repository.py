from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Artista


class ArtistaRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_nombre(self, nombre: str) -> Artista | None:
        return self.db.scalar(select(Artista).where(Artista.nombre == nombre))

    def crear(self, nombre: str) -> Artista:
        artista = Artista(nombre=nombre)
        self.db.add(artista)
        self.db.flush()
        return artista
