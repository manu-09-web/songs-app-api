import re

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class Esquema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, from_attributes=True)


class RegistroEntrada(Esquema):
    nombre: str
    email: str
    password: str

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, v: str) -> str:
        v = v.strip()
        if not v or len(v) > 60:
            raise ValueError("Escribe tu nombre (máximo 60 caracteres)")
        return v

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) > 120 or not EMAIL.match(v):
            raise ValueError("Correo no válido")
        return v

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v.encode()) > 72:
            raise ValueError("La contraseña es demasiado larga")
        return v


class LoginEntrada(Esquema):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError("Escribe tu correo")
        return v

    @field_validator("password")
    @classmethod
    def validar_password(cls, v: str) -> str:
        if not v:
            raise ValueError("Escribe tu contraseña")
        return v


class UsuarioSalida(Esquema):
    id: int
    nombre: str
    email: str


class AuthRespuesta(Esquema):
    access_token: str
    token_type: str = "Bearer"
    usuario: UsuarioSalida
