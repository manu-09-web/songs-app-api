from core.errors import ApiError
from core.security import cifrar_password, crear_token, password_correcta
from models import Usuario
from repositories.usuario_repository import UsuarioRepository
from schemas.auth import AuthRespuesta, LoginEntrada, RegistroEntrada, UsuarioSalida


class AuthService:
    def __init__(self, usuarios: UsuarioRepository):
        self.usuarios = usuarios

    def registrar(self, datos: RegistroEntrada) -> AuthRespuesta:
        if self.usuarios.buscar_por_email(datos.email):
            raise ApiError(409, "EMAIL_EN_USO", "Ese correo ya está registrado")

        usuario = self.usuarios.crear(
            Usuario(
                nombre=datos.nombre,
                email=datos.email,
                password_hash=cifrar_password(datos.password),
            )
        )
        return self._sesion(usuario)

    def iniciar_sesion(self, datos: LoginEntrada) -> AuthRespuesta:
        usuario = self.usuarios.buscar_por_email(datos.email)
        if usuario is None or not password_correcta(datos.password, usuario.password_hash):
            raise ApiError(401, "CREDENCIALES_INVALIDAS", "Correo o contraseña incorrectos")
        return self._sesion(usuario)

    def _sesion(self, usuario: Usuario) -> AuthRespuesta:
        return AuthRespuesta(
            access_token=crear_token(usuario.id),
            usuario=UsuarioSalida.model_validate(usuario),
        )
