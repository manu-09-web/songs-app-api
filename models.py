import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import DECIMAL, Date, Enum, ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class EstadoCancion(str, enum.Enum):
    no_dominada = "no_dominada"
    a_medias = "a_medias"
    dominada = "dominada"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class Artista(Base):
    __tablename__ = "artistas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60), unique=True)


class Cancion(Base):
    __tablename__ = "canciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"))
    artista_id: Mapped[int] = mapped_column(ForeignKey("artistas.id"))
    titulo: Mapped[str] = mapped_column(String(80))
    tonalidad: Mapped[str] = mapped_column(String(4))
    bpm: Mapped[int] = mapped_column(SmallInteger)
    duracion_min: Mapped[Decimal] = mapped_column(DECIMAL(4, 1))
    fecha_ensayo: Mapped[date] = mapped_column(Date)
    estado: Mapped[EstadoCancion] = mapped_column(
        Enum(EstadoCancion, values_callable=lambda e: [x.value for x in e]),
        default=EstadoCancion.no_dominada,
    )
    letra: Mapped[str | None] = mapped_column(Text)

    artista: Mapped[Artista] = relationship(lazy="joined")
    acordes: Mapped[list["CancionAcorde"]] = relationship(
        order_by="CancionAcorde.posicion",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class CancionAcorde(Base):
    __tablename__ = "cancion_acordes"

    cancion_id: Mapped[int] = mapped_column(
        ForeignKey("canciones.id", ondelete="CASCADE"), primary_key=True
    )
    posicion: Mapped[int] = mapped_column(primary_key=True)
    acorde: Mapped[str] = mapped_column(String(8))
