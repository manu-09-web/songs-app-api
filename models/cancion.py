import enum
from datetime import date
from decimal import Decimal

from sqlalchemy import DECIMAL, Date, Enum, ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from models.artista import Artista


class EstadoCancion(str, enum.Enum):
    no_dominada = "no_dominada"
    a_medias = "a_medias"
    dominada = "dominada"


class Cancion(Base):
    __tablename__ = "CANCION"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("USUARIO.id", ondelete="CASCADE"))
    artista_id: Mapped[int] = mapped_column(ForeignKey("ARTISTA.id"))
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
    __tablename__ = "CANCION_ACORDE"

    cancion_id: Mapped[int] = mapped_column(
        ForeignKey("CANCION.id", ondelete="CASCADE"), primary_key=True
    )
    posicion: Mapped[int] = mapped_column(primary_key=True)
    acorde: Mapped[str] = mapped_column(String(8))
