from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Usuario(Base):
    __tablename__ = "USUARIO"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
