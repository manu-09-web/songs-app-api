import re
from datetime import date

from pydantic import field_validator

from models import EstadoCancion
from schemas.base import Esquema

# Nota (A-G), alteración opcional (# o b) y "m" si es menor: C, F#, Bb, Am, F#m
TONALIDAD = re.compile(r"^[A-G][#b]?m?$")
# Nota, alteración, tipo (m, maj, dim, sus…), número (7, 9…) y bajo opcional: Am, G7, Cmaj7, Dsus4, Am/G
ACORDE = re.compile(r"^[A-G][#b]?(m|maj|min|dim|aug|sus|add)?\d{0,2}(/[A-G][#b]?)?$")


class CancionEntrada(Esquema):
    titulo: str
    artista: str
    tonalidad: str
    bpm: int
    duracion_min: float
    fecha_ensayo: date
    estado: str
    acordes: list[str]
    letra: str | None = None

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 80:
            raise ValueError("Escribe el título (máximo 80 caracteres)")
        return v

    @field_validator("artista")
    @classmethod
    def validar_artista(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 60:
            raise ValueError("Escribe el artista (máximo 60 caracteres)")
        return v

    @field_validator("tonalidad")
    @classmethod
    def validar_tonalidad(cls, v: str) -> str:
        v = v.strip()
        if not TONALIDAD.match(v):
            raise ValueError("Tonalidad no válida (ej. Am, F#, Bb)")
        return v

    @field_validator("bpm")
    @classmethod
    def validar_bpm(cls, v: int) -> int:
        if not 40 <= v <= 240:
            raise ValueError("Debe estar entre 40 y 240")
        return v

    @field_validator("duracion_min")
    @classmethod
    def validar_duracion(cls, v: float) -> float:
        if not 0 < v <= 20:
            raise ValueError("Duración no válida")
        return round(v, 1)

    @field_validator("fecha_ensayo")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("La fecha no puede ser futura")
        return v

    @field_validator("estado")
    @classmethod
    def validar_estado(cls, v: str) -> str:
        if v not in [e.value for e in EstadoCancion]:
            raise ValueError("Elige un estado válido")
        return v

    @field_validator("acordes")
    @classmethod
    def validar_acordes(cls, v: list[str]) -> list[str]:
        acordes = [a.strip() for a in v if a.strip()]
        if not 1 <= len(acordes) <= 12:
            raise ValueError("Agrega de 1 a 12 acordes")
        for acorde in acordes:
            if len(acorde) > 8 or not ACORDE.match(acorde):
                raise ValueError(f"Acorde no válido: {acorde}")
        return acordes

    @field_validator("letra")
    @classmethod
    def validar_letra(cls, v: str | None) -> str | None:
        if v is None or not v.strip():
            return None
        if len(v) > 5000:
            raise ValueError("La letra es demasiado larga")
        return v


class CancionSalida(Esquema):
    id: int
    titulo: str
    artista: str
    tonalidad: str
    bpm: int
    duracion_min: float
    fecha_ensayo: date
    estado: str
    acordes: list[str]
    letra: str | None
